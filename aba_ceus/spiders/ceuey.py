import scrapy
from datetime import datetime, timezone

from aba_ceus.items import AbaCeusItem

class CeueySpider(scrapy.Spider):
    name = 'ceuey'
    allowed_domains = ['ceuey.com']
    start_urls = ['https://ceuey.com/ceu-courses/']
    contentful_provider_entry_id = '4WKzGaX5Oz2KQHWUmZzNaF'

    def parse(self, response):

        section_links = response.xpath("//div[contains(@class, 'astra-shop-thumbnail-wrap')]//a/@href").extract()
        raw_links = list(filter(('#').__ne__, section_links)) # removing # links
        raw_links = list(filter(().__ne__, raw_links))  # removing # links

        links = []
        for link in raw_links:
            if '-bundle/' in link:
                pass
            else:
                links.append(link)

        for link in links:
            yield scrapy.Request(url=link, callback=self.create_item)

    def create_item(self, response):

        item = AbaCeusItem()

        item['title'] = response.xpath("//h1[contains(@class, 'product_title entry-title')]/text()").extract_first()
        item['description'] = response.xpath("//div[contains(@class, 'woocommerce-product-details__short-description')]//p/text()").extract()
        item['url'] = response.url
        item['image_urls'] = response.xpath("//img[contains(@class, 'wp-post-image')]/@data-src").extract_first()
        item['price'] = float(response.xpath("//span[contains(@class, 'woocommerce-Price-amount amount')]/text()").extract()[1])
        item['ceu_credits'] = float(response.xpath("//span[contains(@class, 'woocommerce-advanced-product-label product-label label-white')]//span/text()").extract()[0].split(' ')[0])
        item['ceu_media_type'] = "OC"
        item['ceu_type'] = "T2"
        item['crawl_date'] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        item['ceu_provider_slug'] = 'ceuey'

        yield item