###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-23-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Behavior Webinars Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  BehaviorWebinarsSpider(scrapy.Spider):
    name = 'behavior_webinars'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        "https://www.bcbaceus.com/bcba-ceus/"
        ]
    contentful_provider_entry_id = '41wW8Jbem61fh34PA8lAd9'

    def parse(self, response):
        
        links = response.css(".astra-shop-thumbnail-wrap a::attr(href)").extract()
        
        for link in links:   
           yield response.follow(link, self.parse_ceu)
        
    
    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        lst_title = response.css(".product_title.entry-title::text").extract()
        item['title'] = lst_title[0]
        ##
        lst_temp = response.css(".woocommerce-product-details__short-description p ::text, .woocommerce-product-details__short-description p em::text, .woocommerce-product-details__short-description ol li::text ").extract()
        str_temp = ""
        item['description'] = str_temp.join(lst_temp).replace("\t","").strip()
        ##
        item['url'] = response.url
        ##
        item['image_url'] = response.css(".woocommerce-product-gallery__image a::attr(href)").extract()
        ##
        item['price'] = response.css(".price .woocommerce-Price-amount.amount bdi::text").extract()[1]
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        str_cred = "".join(lst_title)
        if "supervision CEU" in str_cred:
            item['ceu_credits'] = str_cred[int(str_cred.find("supervision CEU")) - 2]
        elif "Ethics CEU" in str_cred:
            item['ceu_credits'] = str_cred[int(str_cred.find("Ethics CEU")) - 2]
        elif "Learning CEU" in str_cred:
            item['ceu_credits'] = str_cred[int(str_cred.find("Learning CEU")) - 2]
        elif "CEU" in str_cred:
            item['ceu_credits'] = str_cred[int(str_cred.find("CEU")) - 2]
        else:
            item['ceu_credits'] = None
        ##
        item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = 'Behavior-Webinars'
        ##
        yield(item)    
