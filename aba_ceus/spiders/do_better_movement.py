###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-22-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Do Better Movement Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime


class  Spider(scrapy.Spider):
    name = 'do_better_movement'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://dobettermovement.us/ceu-courses/'
        ]
    contentful_provider_entry_id = '3wWDnH29GkaNVAmggQnDMI'

    headers = {
            "accept"    : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Host"      : "collective.dobettermovement.us",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }


    def __init__ (self):
        scrapy.Request(url="https://dobettermovement.us/ceu-courses/", headers = Spider.headers, callback=self.parse)
    
    def parse(self, response):
        links = response.css(".has_ae_slider.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-6be028b.ae-featured-bg-yes.ae-featured-img-size-woocommerce_single.ae-link-yes.ae-featured-bg-source-post.ae-bg-gallery-type-default::attr(data-ae-url)").extract()

        
        for link in links:   
            # print(link)
            # yield response.follow(link, self.parse_ceu)
            yield scrapy.Request(url=link, headers = Spider.headers, callback=self.parse_ceu)
    
        
    
    

    def parse_ceu (self, response):    
        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        #
        item['title'] = response.css(".product_title.entry-title.elementor-heading-title.elementor-size-default::text").extract()
        #
        #if len(global_ceu_description) <= 0:
        lst_temp = response.css(".woocommerce-product-details__short-description p::text, .woocommerce-product-details__short-description ul li::text").extract()
        if len(lst_temp) <= 0:
            lst_temp = response.css(".woocommerce-product-details__short-description p span::text, .woocommerce-product-details__short-description ol li span::text").extract()
        str_temp = "".join(lst_temp)
        item['description'] = str_temp.replace("\xa0","")    
        ##
        item['url'] = response.url
        ##
        item['image_url'] = response.css(".woocommerce-product-gallery__image a::attr(href)").extract()
        ##
        item['price'] = response.css(".woocommerce-Price-amount.amount bdi::text").extract()[0] 
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        # if "I" in global_credits :
        lst_cred = response.css(".elementor-element.elementor-element-ade2d57.elementor-widget.elementor-widget-text-editor .elementor-text-editor.elementor-clearfix::text").extract()
        str_cred = ""
        if len(lst_cred) > 0:
            str_cred = lst_cred[0]
            if str_cred == "NONE" :
                item['ceu_credits'] = None
            else:
                if "Earn" in str_cred:
                    str_cred = str_cred.replace("Earn up to ","")
                    item['ceu_credits'] = str_cred[:str_cred.find("Learning")]
                elif "Earn" not in str_cred:
                    if str_cred.find("Learning") > 6 :
                        item['ceu_credits'] = str_cred[:str_cred.find("Type")]
                    else:    
                        item['ceu_credits'] = str_cred[:str_cred.find("Learning")]
                else:
                    item['ceu_credits'] = None
        else:
            item['ceu_credits'] = None
        ##
        # if "0" in global_ceu_type:
        lst_type = lst_cred
        str_type = ""
        if len(lst_type) > 0:
            str_type = lst_type[0]
            if "Type" in str_type:
                pos = str_type.find("Type")
                item['ceu_type'] = str_type[pos+5:pos+7]
            else:
                item['ceu_type'] = None
        else:
            item['ceu_type'] = None
        ##
        item['ceu_provider_slug'] = "Do-Better-Movement"
        ##
        yield(item)    
