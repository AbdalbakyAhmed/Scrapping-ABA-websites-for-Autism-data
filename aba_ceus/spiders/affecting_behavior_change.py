###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-21-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V02
## Description  : Affecting Behavior Change Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime


class  AffectingBehaviorChangeSpider(scrapy.Spider):
    name = 'affecting_behavior_Change'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://affecting-behavior-change-ces.thinkific.com/'
        ]
    contentful_provider_entry_id = '17FwfbZS3SgMcAJSaN8wrN'

    def parse(self, response):

        links = response.css(".published.card.course-card::attr(data-card-url)").extract()
        
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
        ##Get next page
        next_page = response.css(".pagination li a::attr(href)").extract()
        if len(next_page) > 0 and next_page[-1] is not '':
            next_page = next_page[-1]  
        else: 
            next_page = None

        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_ceu (self, response):
        item = AbaCeusItem()
        print("request url: {}".format(response.url))
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = response.css(".col-xs-12 .section-banner__text-container h1::text").extract()
        ##
        #if len(global_ceu_description) <= 0:
        lst_temp = response.css(".fr-view p::text").extract()
        str_temp = ""
        item['description'] = str_temp.join(lst_temp)     
        ##
        item['url'] = response.url
        ##
        item['image_url'] = response.css(".fr-view p img::attr(src)").extract()
        ##
        lst_price = response.css(".course-action-buttons__container a::text").extract()
        str_price = ""
        str_price = str_price.join(lst_price)   
        if "free" in str_price:
            item['price'] = "0.0"
        else :
            item['price'] = str_price[-6:]
         
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        lst_cred = response.css(".col-xs-12 .custom-theme .fr-view .fr-view p::text").extract()
        if len(lst_cred) > 0 :
            if "." in lst_cred[0]:
                item['ceu_type'] = lst_cred[0][9]
            else:
                item['ceu_type'] = lst_cred[0][7]
        ##
        lst_temp = response.css(".col-xs-12 .section-banner__text-container p::text").extract()
        if len(lst_temp) > 0:
            if lst_temp[0][1] == '.' :
                item['ceu_credits'] = lst_temp [0][0:3] if 'P' not in lst_temp [0][0:3] else None
            else :
                item['ceu_credits'] = lst_temp [0][0] if 'P' not in lst_temp [0][0] else None
        ##
        item['ceu_provider_slug'] = "Affecting_Behavior_Change"
        ##
        yield(item)    
