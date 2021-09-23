###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-24-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  :  Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  FoxyLearningSpider(scrapy.Spider):
    name = 'foxy_learning'
    start_urls = [
        "https://foxylearning.com/ceus/"
        ]
    contentful_provider_entry_id = '8J7nuhUYF6T1RnmbCLQvn'

    def parse(self, response):
        
        links = response.css(".woocommerce-LoopProduct-link.woocommerce-loop-product__link::attr(href)").extract()
        
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
        next_page = []
        try:
            next_page = response.css(".next.page-numbers::attr(href)").extract()
        except:
            next_page = None
        if len(next_page) > 0 :
            yield scrapy.Request(next_page[0], callback=self.parse)
        
    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        lst_title = response.css(".entry-content .woocommerce-breadcrumb::text").extract()
        item['title'] = ''.join(lst_title).replace("»","").strip() 
        ##
        lst_temp = response.css(".woocommerce-Tabs-panel.woocommerce-Tabs-panel--description.panel.entry-content.wc-tab p::text").extract()
        str_temp = "".join(lst_temp)
        item['description'] = str_temp     
        ##
        item['url'] = response.url
        ##
        item['image_url'] = response.css(".woocommerce-product-gallery__image a::attr(href)").extract()[0]
        ##
        item['price'] = response.css(".summary.entry-summary .price .woocommerce-Price-amount.amount bdi::text").extract()
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        item['ceu_credits'] = response.css(".foxyceus::text").extract()[0][0]
        ##
        item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = 'Foxy_Learning'
        ##
        yield(item)    
