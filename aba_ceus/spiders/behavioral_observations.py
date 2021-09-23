import scrapy
import logging
import re

from aba_ceus.items import AbaCeusItem
from datetime import datetime, timezone
# from price_parser import Price
from scrapy.selector import Selector

class BehavioralObservationsSpider(scrapy.Spider):
    name = 'behavioral_observations'
    allowed_domains = ['behavioralobservations.com']
    start_urls = ['https://behavioralobservations.com/get-ceus/']
    contentful_provider_entry_id = '4WKzGaX5Oz2KQHWUmZzNaF'

    def parse(self, response):
        # urls = response.xpath('//table//a/@href')
        table_rows = response.xpath('//table//tbody//tr').extract()
        # row = response.xpath('//table//tbody//tr').extract()

        for row in table_rows:
            credit_info = Selector(text=row).xpath('//td').extract()[1]

            url = Selector(text=row).xpath('//a/@href').get()
            price = Selector(text=row).xpath("//a//@data-price").get()
            ceu_type = self.parse_ceu_type(credit_info)
            ceu_count = self.parse_ceu_units(credit_info)

            yield scrapy.Request(url=response.urljoin(url), callback=self.create_item,
                                     meta={
                                         'url': url,
                                         'price': price,
                                         'ceu_type': ceu_type,
                                         'ceu_count': ceu_count
                                     }
                                 )

    def create_item(self, response):

        item = AbaCeusItem()

        item['title'] = response.xpath("//h1//span/text()").extract_first()
        item['description'] = response.xpath("//div[contains(@class, 'entry-content content')]//p/text()").extract()
        item['url'] = response.meta.get('url')
        item['image_urls'] = None
        item['price']= float(self._parse_price(response.xpath("//span[contains(@class, 'edd-add-to-cart-label')]/text()").extract_first()))
        item['ceu_credits']= float(1)
        item['ceu_media_type'] = "OC"
        item['ceu_type'] = response.meta.get('ceu_type')
        item['crawl_date'] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        item['ceu_provider_slug'] = 'behavioral-observations'

        yield item

    def _parse_price(self, credit_info):
        return int(Price.fromstring(credit_info).amount_float)

    def parse_ceu_type(self, credit_info):

        if Selector(text=credit_info).xpath('//em//strong/text()').extract():

            ceu_type = Selector(text=credit_info).xpath('//em//strong/text()').extract_first()

            if ceu_type == 'Ethics':
                return 'ET'
            elif ceu_type == 'Supervision':
                return 'SV'
            else:
                logging.warning('type error, not listed.')
                raise('type error, not listed.')
        else:
            return 'T2'

    def parse_ceu_units(self, credit_info):
        return float(credit_info.split(':')[1].lstrip().split('<')[0])