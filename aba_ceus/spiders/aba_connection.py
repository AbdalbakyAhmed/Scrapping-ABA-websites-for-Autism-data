###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10--2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : ABA Connection Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  AbaConnectionSpider(scrapy.Spider):
    name = 'aba_connection'
    start_urls = [
        "https://www.abaconnection.com/all-courses/categories/view"
        ]
    contentful_provider_entry_id = ''

    def parse(self, response):
        
        links = response.css(".description_guru .uk-button::attr(href)").extract()
        
        for link in links:   
            yield response.follow(link, self.get_category_links)
        
    def get_category_links (self, response):
        ceu_links = response.css(".readon .uk-button::attr(href)").extract()
        for link in ceu_links:
            yield response.follow(link, self.parse_ceu)

    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        #
        lst_padding = response.css(".uk-list.uk-padding-remove li::text").extract()
        while " " in lst_padding:
            lst_padding.remove(" ")
        #
        item['date_published'] = lst_padding[1].strip()
        ##
        item['title'] = response.css(".uk-overlay-panel.uk-overlay-top h2::text").extract()
        ##
        lst_temp = response.css(".course_view_description p::text").extract()
        item['description'] = "".join(lst_temp)     
        ##
        item['url'] = response.url
        ##
        lst_temp_img = response.css(".uk-cover-background.gru-cover::attr(style)").extract()[0].split()
        item['image_url'] = lst_temp_img[0].strip("background-image:url('")[:-3] 
        ##
        lst_price = lst_padding[-1].split()
        if lst_price[0] == "$" :
            item['price'] = lst_price [1]
        else:
            item['price'] = None
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        try:
            lst_temp_cred = response.css(".uk-overlay-panel.uk-overlay-top h2::text").extract()[0].lower().split()
            ignore_tuple = ("ethics", "ethics)", "unit", "unit)","units", "units)", "credit","-", "credit)","credits", "supervision", "total")
            for ign in ignore_tuple :
                while ign in lst_temp_cred:
                    lst_temp_cred.remove(ign)
            new_lst = lst_temp_cred
            item['ceu_credits'] = new_lst[-1].replace("(","") if "library" not in new_lst[-1] else None
        except:
            item['ceu_credits'] = None
        ##
        item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = 'ABA-Connection'
        ##
        yield(item)    
