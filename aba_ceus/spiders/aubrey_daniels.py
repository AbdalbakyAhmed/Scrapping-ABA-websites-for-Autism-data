###########################################################################
## Author       : Abdelbaky Ahmed   "Upwork Freelancer"
## Date         : 10-19-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Aubrey Daniels Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime

class AubreyDanielsSpider (scrapy.Spider):
    name = 'aubrey_daniels'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://www.aubreydaniels.com/catalog/categories/bacb-ce-courses'
        ]
    contentful_provider_entry_id = '2vm3mcUZ9JOi1y6jO5tsvN'

    def parse(self, response):
        
        links = response.css(".media_element a::attr(href)").extract()
        
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
    def parse_ceu (self, response):
        item = AbaCeusItem()
        
        item['crawl_date'] = get_datetime()

        temp_title = response.css("title::text").extract()[0]
        item['title'] = temp_title[1:-8] 
        # print("Title: " + str(item['title']))
        
        count = 0
        temp = response.css(".field-item.even p::text, .field-item.even p span::text").extract()
        for i in temp:
            if i == "Topics covered in this course include:" :
                break
            count += 1
        temp = temp[:count]
        d_str  = ""
        d_str = d_str.join(temp)
        
        item['description'] = d_str
        # print("description: " + d_str)
        
        item['url'] = response.url
        # print("url: " + str(item['url']))
        
        item['image_url'] = 'https://www.aubreydaniels.com' + str(response.css(".field-item.even img::attr(src)").extract()[0])
        # print("IMAGE URL: {}".format(str(item['image_url'])))

        item['price']= response.css(".uc-price::text").extract()[1]
        
        item['ceu_credits']= temp_title[-7:-4]
        item['ceu_media_type'] = "Podcast" # Set static as all podcasts
        
        try:
            ceu_type = response.css(".rtf-prodtitle em::text").extract()[1]
            ceu_type = ceu_type[-11:-5]
            item['ceu_type'] = ceu_type
        except :
            ceu_type = response.css(".field-item.even p strong::text").extract()[1]
            ceu_type = ceu_type[-11:-5]
            item['ceu_type'] = ceu_type    
        
        
        item['ceu_provider_slug'] = "Aubrey-Daniels"
        yield(item)


        # if temp:
        #     for i in temp:
        #         if i == "Topics covered in this course include:" :
        #             break
        #         count += 1
        #     temp = temp[:count]
        #     d_str  = ""
        #     d_str = d_str.join(temp)
        # else :
        #     temp = response.css(".field-item.even p::text").extract()
        #     for i in temp:
        #         if i == "Topics covered in this course include:" :
        #             break
        #         count += 1
        #     temp = temp[:count]
        #     d_str  = ""
        #     d_str = d_str.join(temp)
