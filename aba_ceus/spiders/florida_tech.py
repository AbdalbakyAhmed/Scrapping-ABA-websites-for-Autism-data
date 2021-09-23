###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-21-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V02
## Description  : Florida Tech Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
#from pyquery import PyQuery as pq

class  FloridaTechSpider(scrapy.Spider):
    name = 'florida_tech'
    ## allowed_domains = ['https://www.fit.edu/continuing-education/applied-behavior-analysis/ce-courses--workshops/ces-by-topics/']
    start_urls = [
        'https://www.fit.edu/aba-online/ce-courses-workshops/ces-by-credit-hours/'
        ]
    contentful_provider_entry_id = '19kv5xtHv5bPpS3shCuFJ4'

    def parse(self, response):
        #selector = pq(response.body)
        #Links = [pq(x).attr('href') for x in selector('.ceuBtn')]
        #selector('aa').text()
        links = response.css(".ceuBtn::attr(href)").extract()
        
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
    
    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        lst_temp = response.css(".clsCourseInfo .clsCourseInfo_NameText::text, .hero-head.h1::text").extract()  
        item['title'] = lst_temp[0].strip()
        ##
        
        lst_temp = response.css(".clsCourseInfo_DescText td p span::text, .clsCourseInfo_DescText td ul li span::text").extract()
        if len(lst_temp) <= 0:
            lst_temp = response.css(".container.product-details div p span::text , .container.product-details div ul li span::text").extract() 
        
        ign_list = [
            "\r\n", "   ", "\xa0" 
        ]
        if len(lst_temp) > 0:
            str_temp = ""
            new_lst = []
            
            for i in lst_temp:
                new_lst.append(i.strip())
            str_temp = str_temp.join(new_lst)

            for j in ign_list:
                str_temp.replace(j, "")

            item['description'] = str_temp     
        
        ##
        item['url'] = response.url
        ##
        
        img_tmp = list()
        img_tmp = response.css(".clsCourseInfo_DescText td img::attr(src)").extract()
        if len(img_tmp) <= 0:
            img_tmp = response.css(".image-wrapper::attr(style)").extract()
            if len(img_tmp) > 0 :
                pos = img_tmp[0].find("https")
                item['image_url'] = img_tmp[0][pos:-1]
        else:                    
            item['image_url'] = img_tmp[0] 
        
        ##
        price_tmp = list()
        price_tmp = response.css(".clsCourseInfo_PriceText ::text").extract()
        if len(price_tmp) <= 0:
            price_tmp = response.css(".btn.btn-info.btn-lg.btn-action ::text").extract()
            if len(price_tmp) > 0:
                item['price'] = price_tmp[0][:-6]
            else:
                None
        else:
            item['price'] = price_tmp[0]
        
        ##
        item['ceu_media_type'] = "Podcast"
        
        ##
        # if "I" in global_credits :
        temp_cont = response.css(".clsCourseInfo_DescText tr td span::text, .clsCourseInfo_DescText tr td::text").extract()
        if len(temp_cont) <= 0:
            temp_cont = response.css(".container.product-details span::text, .container.product-details p::text").extract()
            count = 0
            flg_type_found = False
            for i in temp_cont[:4]:
                if "type" in i:
                    flg_type_found = True
                    break
                count += 1
            if flg_type_found:
                temp_cont[count] = temp_cont[count].strip().replace(": ","")    
                if temp_cont[count - 1].isnumeric():
                    item['ceu_credits'] = temp_cont[count -1]    
                else:
                    item['ceu_credits'] = temp_cont[count][:3].replace("t","") if "." in temp_cont[count] else temp_cont[count][0].replace("t","")
                pos = temp_cont[count].find("type")
                item['ceu_type'] = temp_cont[count][pos+5]
            else:
                item['ceu_credits'] = None
                item['ceu_type']    = None

        else:
            count = 0
            flg_type_found = False
            for i in temp_cont[:5]:
                if "type" in i:
                    flg_type_found = True
                    break
                count += 1
            if flg_type_found:
                temp_cont[count] = temp_cont[count].strip().replace(": ","")
                if temp_cont[count - 1].isnumeric():
                    item['ceu_credits'] = temp_cont[count -1]    
                else:
                    item['ceu_credits'] = temp_cont[count][:3].replace("t","") if "." in temp_cont[count] else temp_cont[count][0].replace("t","")
                pos = temp_cont[count].find("type")
                item['ceu_type'] = temp_cont[count][pos+5]
            else:
                item['ceu_credits'] = None
                item['ceu_type']    = None

        ##
        item['ceu_provider_slug'] = "Florida_Tech"
        ##
        yield(item)    
