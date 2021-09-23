###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10--2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Behavior University Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  BehaviorUniversitySpider(scrapy.Spider):
    name = 'behavior_university'
    start_urls = [
        "https://behavioruniversity.com/bcba-ceu"
        ]
    contentful_provider_entry_id = '4NDPSWCiwIJfHXqlUG07ST'

    def parse(self, response):
        
        links = response.css(".product-thumb.box .caption h4 a::attr(href)").extract()
        
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
        next_page = []
        try:
            next_page = response.css(".pagination .active span::text").extract() 
        except :
            next_page = None
        if len(next_page) > 0:
            page_num = int(next_page[0]) + 1
            link = "https://behavioruniversity.com/bcba-ceu?page=" + str(page_num)
            yield scrapy.Request(link, callback=self.parse)
    
    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = "".join(response.css("#content h1::text").extract())
        ##
        lst_temp = response.css(".tab-pane.active.lead p::text, .tab-pane.active.lead p span::text, .tab-pane.active.lead p font::text").extract() 
        str_temp = ""
        item['description'] = str_temp.join(lst_temp).replace("\xa0", " ")   
        ##
        item['url'] = response.url
        ##
        try:
            item['image_url'] = "https://behavioruniversity.com/" + response.css(".tab-pane.active.lead img::attr(src)").extract()[0]
        except:
            item['image_url'] = None
        ##
        item['price'] = response.css(".col-sm-4 .list-unstyled li h2::text").extract()
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        item['ceu_credits'] = response.css(".product-info.list-unstyled li::text").extract()[2][:2] 
        ##
        item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = "Behavior-University"
        ##
        yield(item)    
