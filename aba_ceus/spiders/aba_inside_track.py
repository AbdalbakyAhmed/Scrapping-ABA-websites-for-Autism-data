
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime

class AbaInsideTrackSpider(scrapy.Spider):
    name = 'aba_inside_track'
    allowed_domains = ['www.abainsidetrack.com']
    start_urls = ['https://www.abainsidetrack.com/get-ceus/']
    contentful_provider_entry_id = '55ZopWs8MM5L20vjuGpFle'

    def parse(self, response):

        links = response.xpath('//a/@href')

        for link in links:
            url = link.get()
            full_url = response.urljoin(url)

            if '/get-ceus/' in url:

                yield scrapy.Request(url=full_url, callback=self.create_item)

    def create_item(self, response):

        item = AbaCeusItem()

        item['title'] = response.xpath("//h1[contains(@class, 'ProductItem-details-title')]/text()").extract_first()
        item['description'] = response.xpath("//div[contains(@class, 'sqs-block-content')]//p/text()").extract()
        # if not item['description']:
        #     item['description'] = response.xpath("//div[contains(@class, 'product-description')]//p/text()").extract()
        item['url'] = response.url
        item['image_urls'] = [response.xpath("//div[contains(@class, 'ProductItem-gallery-slides-item sqs-image-zoom-area')]//img/@data-src").extract_first()]
        item['price']= float(response.xpath("//span[contains(@class, 'sqs-money-native')]/text()").extract_first())
        item['ceu_credits']= float(1)
        item['ceu_media_type'] = "Podcast" # Set static as all podcasts
        item['ceu_type'] = "Type 2"
        item['crawl_date'] = get_datetime()
        item['ceu_provider_slug'] = "aba-inside-track"

        yield item


