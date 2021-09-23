###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-24-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : VBMAPP APP Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  VbmappSpider(scrapy.Spider):
    name = 'vbmapp'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        "https://www.vbmappapp.com/products_services/online_training"
        ]
    contentful_provider_entry_id = ''

    def parse(self, response):
        
        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = response.css(".training.single_column_layout .container legend::text").extract()
        ##
        lst_temp = response.css(".training_info.prose div p::text, .training_info.prose div p b u::text").extract() 
        str_temp = "".join(lst_temp).replace("\n","")
        item['description'] = str_temp
        ##
        item['url'] = response.url
        ##
        item['image_url'] = None
        ##
        pos = str_temp.find('$')
        item['price'] = str_temp[pos:int(pos+6)]
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        pos = str_temp.find("BACB")
        item['ceu_credits'] = str_temp[ pos - 3 : pos - 1 ]
        ##
        item['ceu_type'] = str_temp[pos + 10]
        ##
        item['ceu_provider_slug'] = "VB-MAPP"
        ##
        yield(item)    

        
    
   