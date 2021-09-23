###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-23-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Relias Academy Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  ReliasAcademySpider(scrapy.Spider):
    name = 'relias_academy'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        "https://reliasacademy.com/rls/store/bcba-online-continuing-education?utm_medium=cpc&campaignid=1700266237&adgroupid=73130151544&adid=330246521684&gclid=EAIaIQobChMIk8b-sYjE6gIVR9bACh3F6gUxEAAYAiAAEgI6wfD_BwE"
        ]
    contentful_provider_entry_id = '61N2m7lXvrBrZSbUpAWuJn'

    images_list = []    
    clss_count = 0


    def parse(self, response):
        
        links = response.css(".col-xs-12.col-sm-6.col-md-4 .block div a::attr(href) , .product-description section p a::attr(href)").extract()
        count = 0
        while count < len(links) :
            if 's.jsp' in links[count]:
                links.pop(count)
                count -= 1            
            count += 1
        
        img_lst = response.css(".col-md-12 .col-xs-12.col-sm-6.col-md-4 .block img::attr(src)").extract()
        ##
        count = 0
        while count < len(img_lst) :
            if 'ing.gif' in img_lst[count]:
                img_lst.pop(count)
                count -= 1            
            count += 1
        ReliasAcademySpider.images_list = img_lst
        ##
        print("Links: \n {}".format(links))
        
        for link in links:
            yield response.follow(link, self.parse_ceu)
            # ReliasAcademySpider.class_cnt += 1  if ReliasAcademySpider.class_cnt < len(ReliasAcademySpider.images_list) else 100
        
    
    def parse_ceu (self, response):
        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = response.css(".page-title span::text, .h1-allaccess span::text").extract()
        ##
        lst_temp = response.css("#longDescription span::text, .h2-allaccess::text").extract() 
        str_temp = ""
        item['description'] = str_temp.join(lst_temp).strip()
        ##
        item['url'] = "https://reliasacademy.com" + str (response.url)
        ##
        # item['image_url'] = ReliasAcademySpider.images_list[ int(ReliasAcademySpider.class_cnt) ] if ReliasAcademySpider.class_cnt < len(ReliasAcademySpider.images_list) else None
        if ReliasAcademySpider.clss_count < len(ReliasAcademySpider.images_list):
            item['image_url'] = ReliasAcademySpider.images_list[ReliasAcademySpider.clss_count]
            ReliasAcademySpider.clss_count += 1
        else:
            item['image_url'] = None    
        ##
        item['price'] = response.css("#productPrice span::text").extract()[3].strip()
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        item['ceu_credits'] = None
        ##
        item['ceu_type'] = None #Site doesn't contain Type
        ##
        item['ceu_provider_slug'] = 'Relias_Academy'
        ##
        yield(item)    
