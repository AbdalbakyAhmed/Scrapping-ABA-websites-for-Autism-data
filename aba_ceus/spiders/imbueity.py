###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-25-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Imbueity Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  ImbueitySpider(scrapy.Spider):
    name = 'imbueity'
    start_urls = [
        "https://imbueity.com/supervision/continuing-education-ceus/"
        ]
    contentful_provider_entry_id = '2tQ1tfSHi8aASTKY1PNjqm'

    def parse(self, response):
        
        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = response.css(".entry-content h3::text").extract()
        ##
        lst_temp = response.css(".entry-content p::text, .entry-content strong::text").extract()
        pos = 0
        for i in lst_temp:
            if "Abstract" in i:
                break
            pos += 1
        str_temp = "".join( lst_temp [ pos+1 : ] )
        item['description'] = str_temp
        ##
        item['url'] = response.url
        ##
        item['image_url'] = response.css(".entry-header img::attr(src)").extract() 
        ##
        pos = 0
        for i in lst_temp:
            if "Cost" in i:
                break
            pos += 1
        temp = lst_temp[pos].split()    
        item['price'] = temp[1]
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        temp = response.css(".entry-content p em::text").extract()[0].split()
        item['ceu_credits'] = temp[0]
        ##
        item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = 'Imbueity'
        ##
        yield(item)  
