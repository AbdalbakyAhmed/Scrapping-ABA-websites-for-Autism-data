###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-23-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Behavior Development Solutions Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  BehaviorDevelopmentSolutionsSpider(scrapy.Spider):
    name = 'behavior_development_solutions'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        "https://www.behaviordevelopmentsolutions.com/bacb-ace-type-ii-ce-courses"
        ]
    contentful_provider_entry_id = '3sKAuhWQRL8hNpC9JFdU8j'

    def parse(self, response):
        
        links = response.css(".product-title a::attr(href)").extract() 
        
        for link in links:   
           yield response.follow(link, self.parse_ceu)
        
        next_page = response.css(".next-page a::attr(href)").extract()
        next_page = next_page[0] if len (next_page) > 0 else None

        if next_page:
            yield response.follow(next_page, self.parse)        
    
    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = response.css(".product-name h1::text").extract()
        ##
        lst_temp = response.css(".short-description::text, .short-description b::text").extract()
        str_temp = "".join(lst_temp) 
        item['description'] = str_temp 
        ##
        item['url'] = str(response.url)
        ##
        item['image_url'] = response.css(".gallery .picture img::attr(src)").extract()
        ##
        item['price'] = response.css(".product-price span::attr(content)").extract()[0]
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        if "Earn" in str_temp:
            pos = int ( str_temp.find('Earn') ) 
            item['ceu_credits'] = str_temp[ pos+5 : pos+8 ] if str_temp[pos + 6] == "." else str_temp[pos+5]
        elif "Learning Supervision" in str_temp:
            pos = int ( str_temp.find("Learning Supervision") )
            item['ceu_credits'] = str_temp[ pos-4 : pos-1 ] if str_temp[pos - 3] == "." else str_temp[pos-2]
        elif "Learning CE" in str_temp:
            pos = int ( str_temp.find("Learning CE") )
            item['ceu_credits'] = str_temp[ pos-4 : pos-1 ] if str_temp[pos - 3] == "." else str_temp[pos-2]      
        elif "Learning Ethics" in str_temp:
            pos = int ( str_temp.find("Learning Ethics") )
            item['ceu_credits'] = str_temp[ pos-4 : pos-1 ] if str_temp[pos - 3] == "." else str_temp[pos-2]
        else:
            item['ceu_credits'] = None
        ##
        item['ceu_type'] = None #Site doesn't contain Type
        ##
        if "LIVE" in str_temp:
            item['event_published'] = "LIVE on" + str (str_temp[ int(str_temp.find("occur on")) + 9 : int(str_temp.find("Time")) + 4])
        else:
            item['event_published'] = None
        ##
        item['ceu_provider_slug'] = 'Behavior-Development-Solutions'
        ##
        yield(item)    
