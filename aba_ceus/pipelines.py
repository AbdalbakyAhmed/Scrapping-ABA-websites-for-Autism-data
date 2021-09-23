# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
from io import StringIO  # python3; python2: BytesIO
from datetime import datetime
import sys
import requests
import json
import logging

import boto3
from botocore.exceptions import ClientError

import pandas as pd

import contentful_management

class AbaCeusPipeline:
    def process_item(self, item, spider):
        return item

class S3PipelineCSV:
    """
    Scrapy pipeline to store items into S3 bucket with CSV format format.
    Unlike FeedExporter, the pipeline has the following features:
    * The pipeline stores items by chunk.
    * Support GZip compression.
    """

    def __init__(self, settings, stats):

        self.stats = stats
        self.aws_profile = settings['AWS_PROFILE']
        self.aws_session = boto3.session.Session(profile_name=self.aws_profile)
        self.s3 = self.aws_session.resource('s3')
        self.s3_bucket_name = 'abanerd-default-rawdata-crawler'
        self.s3_path = 'scrapy/aba_ceus/' # {self.s3_path}/{spider_name}/{spidername}-{timestamp}.csv
        self.max_chunk_size = settings.getint('S3PIPELINE_MAX_CHUNK_SIZE', 100)
        self.items = []
        self.chunk_number = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.stats)

    def process_item(self, item, spider):
        """
        Process single item. Add item to items and then upload to S3 if size of items
        >= max_chunk_size.
        """
        self.items.append(item)

        return item

    def open_spider(self, spider):
        """
        Callback function when spider is open.
        """
        # Store timestamp to replace {time} in S3PIPELINE_URL
        self.ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')

    def close_spider(self, spider):
        """
        Callback function when spider is closed.
        """
        # Upload items to S3.
        self._upload_csv_to_s3(spider)

    def _make_csv_file(self):
        """
        Build file object from items.
        """
        data = []

        for item in self.items:
            data.append(dict(item))

        df = pd.DataFrame(data)

        csv_buffer = StringIO()

        df.to_csv(csv_buffer)

        return csv_buffer.getvalue()

    def _upload_csv_to_s3(self, spider):
        """
        Do upload items to S3.
        """

        if not self.items:
            self.stats.inc_value('pipeline/s3/items/fail')
            raise

        file = self._make_csv_file()

        file_path = self.s3_path + '{}/{}-crawldata-ceus-{}.csv'.format(
                spider.name,
                spider.name,
                time.strftime("%Y%m%d-%H%M%S")
            )

        try:
            response = self.s3.Object(self.s3_bucket_name, file_path).put(Body=file)
            self.stats.inc_value('pipeline/s3/success')
            return response

        except ClientError:
            self.stats.inc_value('pipeline/s3/client_error/fail')
            raise
        except:
            self.stats.inc_value('pipeline/s3/fail')
            raise

# from itemadapter import ItemAdapter # do I need this?




class ContentfulPipeline:

    def __init__(self, settings, stats):
        self.contentful_api_token = settings['CONTENTFUL_MANAGEMENT_API_TOKEN']
        self.contentful_api_content_token = settings['CONTENTFUL_MANAGEMENT_CDN_API_TOKEN']
        self.space_id = settings['CONTENTFUL_SPACE_ID']
        self.enviorment_id = settings['CONTENTFUL_ENV_ID'] # Defaults to `master`
        self.content_type = settings['CONTENTFUL_CONTENT_TYPE_ID']
        self.force_update = settings['CONTENTFUL_FORCE_UPDATE']

    @classmethod
    def from_crawler(cls, crawler):

        return cls(crawler.settings, crawler.stats)

    def open_spider(self, spider):
        self.client = contentful_management.Client(self.contentful_api_token)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):

        ceu_exists, entries = self.is_ceu_present(item['title'])

        if not ceu_exists:
            content = self.ceu_content_type_attributes(item, spider)
            self.make_ceu_entry(content)
        elif self.force_update:
            entry_id = entries[0]['sys']['id']
            content = self.ceu_content_type_attributes(item, spider)
            self.update_ceu_entry(content, entry_id)
        else:
            logging.warning('\"{}\" was already present in contentful. Force update set to `{}`. Skipping...'.format(item['title'], self.force_update))
            pass

    def ceu_content_type_attributes(self, item, spider):
        # https://www.contentful.com/developers/docs/concepts/links/

        provider_entry_id = spider.contentful_provider_entry_id
        description = "\n".join(item['description'])
        media_format = self._make_list(item['ceu_media_type'],)
        ceu_type = self._make_list(item['ceu_type'],)

        try:
            s3_path_filename = item['images'][0]['path'].split("/")[1]
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        entry_attributes = {
            'content_type_id': self.content_type,
            'fields': {
                'title': {
                    "en-US": item['title'],
                },
                'description': {
                    "en-US": description,
                },
                'link': {
                    "en-US": item['url'],
                },
                'price': {
                    "en-US": float(item['price']),
                },
                'ceuCount': {
                    "en-US": float(item['ceu_credits']),
                },
                'ceuFormat': {
                    "en-US": media_format,
                },
                'ceuType': {
                    "en-US": ceu_type,
                },
                'logoS3Path': {
                    "en-US": s3_path_filename,
                },
                'ceuProvider': {
                    "en-US": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": provider_entry_id
                        }
                    }
                }
            }
        }

        return entry_attributes

    def is_ceu_present(self, title):

        base_url = "https://cdn.contentful.com/"

        url = base_url + "spaces/{}/environments/{}/entries?access_token={}&content_type={}&fields.title={}".format(
            self.space_id, self.enviorment_id, self.contentful_api_content_token, self.content_type, title
        )

        payload = {}
        headers = {}

        request = requests.request("GET", url, headers=headers, data=payload)

        request_json = request.json()

        return request_json['total'], request_json['items']

    def make_ceu_entry(self, content, entry_id=None):

        try:

            entry = self.client.entries(self.space_id, self.enviorment_id).create(entry_id, content)
            entry.publish()
            if entry.is_published:
                return True
            else:
                return False

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def update_ceu_entry(self, content, entry_id):

        try:
            entry = self.client.entries(self.space_id, self.enviorment_id).find(entry_id)
            entry.update(content)
            entry.save()
            entry.publish()

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def _make_list(self, object):
        if isinstance(object, list):
            return object
        else:
            return [object]

    # def is_ceu_present(self, title):
    #     return bool(self.content_client.entries({'content_type': self.content_type, 'fields.title': title}))
