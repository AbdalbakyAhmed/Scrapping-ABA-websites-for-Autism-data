###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-20-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : University of West Florida Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime

global_ceu_type = ''
global_credits = ''
global_ceu_description = ''

class  UniversityWestFloridaSpider(scrapy.Spider):
    name = 'university_west_florida'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://uwf.behavior.org/list-courses/#tab-supervision'
        ]
    contentful_provider_entry_id = '1v3ZK3ZUbOU6Vhnh0Fekq5'

    def parse(self, response):
        links = response.css(".ld-entry-title.entry-title a::attr(href)").extract()

        # remove duplicated links
        links = list(dict.fromkeys(links)) 
        
        for link in links:   
            yield response.follow(link, self.check_run_link)
        
    
    def check_run_link(self, response):
        global global_ceu_type
        global global_credits 
        global global_ceu_description 

        global_ceu_type = ' '
        global_credits = ' '
        global_ceu_description = ' '
        
        ##
        # lst_temp_d = response.css(".learndash_content p::text, .learndash_content p strong::text, .learndash_content p span::text").extract()
        # str_temp_d = ' '
        # global_ceu_description = str_temp_d.join(lst_temp_d)

        # if len(global_ceu_description) <= 0:
        #     lst_temp_d = response.css(".learndash_content p::text, .learndash_content p strong::text, .learndash_content p span::text").extract()
        #     str_temp_d = ' '
        #     global_ceu_description = str_temp_d.join(lst_temp_d)

        ##    
        temp_content = response.css(".learndash_content p strong em::text, .learndash_content p em strong::text").extract() 
        ##
        if len(temp_content) > 0:
            if "0" in temp_content[0] or ".5" in temp_content[0]:
                global_ceu_type = temp_content[0][:3]

            if "I" in temp_content[0]:
                global_credits = temp_content[0][9:11]
        ##
                        
        try:
            join_link = response.css(".btn-join::attr(href)").extract()[0]
            yield response.follow(join_link, self.parse_ceu)    
        except:
            pass 
    
    
    def parse_ceu (self, response):

        global global_ceu_type
        global global_credits 
        global global_ceu_description 

        check_title = response.css(".entry-title::text").extract()
        if len(check_title) > 0:
            if "Oops" in check_title[0] :
                pass
            else:
                item = AbaCeusItem()
                ##
                item['crawl_date'] = get_datetime()
                ##
                item['title'] = response.css(".product_title.entry-title::text").extract()[0]
                ##
                #if len(global_ceu_description) <= 0:
                lst_temp = response.css(".woocommerce-product-details__short-description p::text, .woocommerce-product-details__short-description p span::text").extract()
                str_temp = ""
                item['description'] = str_temp.join(lst_temp) 
                # item['description'] = global_ceu_description    
                ##
                item['url'] = response.url
                ##
                item['image_url'] = response.css(".woocommerce-product-gallery__image--placeholder img::attr(src)").extract()[0]
                ##
                item['price'] = response.css(".woocommerce-Price-amount.amount::text").extract()[0]
                ##
                item['ceu_media_type'] = "Podcast"
                ##
                # if "I" in global_credits :
                item['ceu_type'] = global_credits
                # else:
                #     item['ceu_credits'] = "II"    
                ##
                # if "0" in global_ceu_type:
                item['ceu_credits'] = global_ceu_type
                # else:
                #     item['ceu_type'] = "1.0"
                ##
                item['ceu_provider_slug'] = "University-West-florida"  
                ##
                global_ceu_type = ' '
                global_credits = ' '
                global_ceu_description = ' '
                ##
                yield(item)    

        else:
            pass    
        