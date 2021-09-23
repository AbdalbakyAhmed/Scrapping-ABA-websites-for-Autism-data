###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-20-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : ABA Technologies Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime

class ABATechnologiesSpider (scrapy.Spider):
    name = 'aba_technologies'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://abatechnologies.com/continuing-education/'
        ]
    contentful_provider_entry_id = '1yPZPbv8PAT7a4T1yEkN7h'

    def parse(self, response):
        links = response.css(".itemTitle.kl-blog-item-title a::attr(href)").extract()  
        
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
    def parse_ceu (self, response):
        item = AbaCeusItem()

        item['crawl_date'] = get_datetime()

        item['title'] = response.css(".ce-title.page-title::text").extract()

        count = 0
        lst_temp = response.css(".ce-body p span::text").extract()
        for i in lst_temp:
            if i == "What you’ll learn in the course and be able to do afterward:\xa0":
                break
            count += 1    
        lst_temp = lst_temp[:count]
        str_d = ""
        str_d = str_d.join(lst_temp)

        item['description'] = str_d
        # print("description: " + str_d)

        item['url'] = response.url
        # print("url: " + str(item['url']))

        item['image_url'] = response.css(".ce-image img::attr(src)").extract()[0] 
        # print("IMAGE URL: {}".format(str(item['image_url'])))

        item['price'] = response.css(".ce-price::text").extract()[0][1:]

        str_cred = response.css(".ce-credit::text").extract()[0]
        item['ceu_credits'] = str_cred[ 1 : ( str_cred.find('B') - 1 ) ]

        item['ceu_media_type'] = "Podcast" # Set static as all podcasts

        #item['ceu_type'] = None        ##Doesn't exist in this site

        item['ceu_provider_slug'] = "ABA-Technologies"        

        yield(item)
