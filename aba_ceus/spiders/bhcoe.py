###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-23-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : BHCOE Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
import json

class  BHCOESpider(scrapy.Spider):
    name = 'bhcoe'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://bhcoe.org/behavioral-health-virtual-academy/'
        ]
    contentful_provider_entry_id = '4QTJvEaxnrDTmMg75sDQpr'

    varr = ""

    def parse(self, response):
        links       = response.css(".dp-post-excerpt a::attr(href)").extract()
        images      = response.css(".dp_ppp_post_thumb::attr(src)").extract()
        title       = response.css(".entry-title a::text").extract()
        description = response.css(".dp-post-excerpt::text").extract()  
        count = 0
        item = AbaCeusItem()
        ##
        while  count < len(links) :
            item['crawl_date'] = get_datetime()
            ##
            item['title'] = title[count]
            ##
            item['description'] = description[count] + "*Free for BHCOE members."
            ##
            item['image_url'] = images[count]
            ##
            item ['url'] = links[count]
            ##
            item['ceu_provider_slug'] = 'BHCOE'
            ##
            count += 1
            yield(item)
