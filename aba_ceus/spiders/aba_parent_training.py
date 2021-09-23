###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-24-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : ABA Parent Training Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  ABAParentTrainingSpider(scrapy.Spider):
    name = 'aba_parent_training'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        "https://www.abaparenttraining.com/?offset=2562441914824&format=main-content"
        ]
    contentful_provider_entry_id = '4Ma6omQeVmotq2SYhTcA40'

    def parse(self, response):
        
        links = response.css(".entry-title.entry-title--list.p-name a::attr(href)").extract()
        # print("LINKS: \n {} \n \n length = {} ".format( links, len(links) ) )
        
        for link in links:
            yield response.follow(link, self.parse_ceu)
        
        ##
        try:
            next_load = response.css(".load-more-wrapper .load-more::attr(href)").extract()
        except :
            next_load = []
        
        if len(next_load) > 0:
            # print("next_load:.{}".format(next_load[0][ next_load.find("offest"):]))
            temp = next_load[0]
            next_url = "https://www.abaparenttraining.com" + str(temp) + "&format=main-content"
            # print ("next_url: {}".format(next_url) ) 
            yield scrapy.Request(next_url, callback = self.parse)

    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['date_published'] = response.css(".blog-item-title .dt-published.date-callout::attr(datetime)").extract()
        ##
        item['title'] = response.css(".blog-item-title h2::text").extract()
        ##
        lst_temp = response.css(".sqs-block-content p::text").extract()
        str_temp = ""
        item['description'] = str_temp.join(lst_temp)     
        ##
        item['url'] = response.url
        ##
        item['image_url'] = response.css(".blog-item-banner-image img::attr(data-src)").extract() 
        ##
        item['price'] = None
        ##
        item['ceu_media_type'] = "Podcast" # Article
        ##
        item['ceu_credits'] = None
        ##
        item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = "ABA Parent Training"
        ##
        yield(item)    
