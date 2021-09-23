###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-24-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V03
## Description  : Special Learning  Inc. Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime
# import json

class  SpecialLearningSpider(scrapy.Spider):
    name = 'special_learning'
    start_urls = [
        "https://store.special-learning.com/products"
        ]
    contentful_provider_entry_id = '12wtzchmsGz7Uf300QaOs'

    def parse(self, response):
        
        links = response.css(".product_thumb::attr(href)").extract()
        # print("links: \n {}".format(links))
        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
        last_page = response.css(".btn.btn-small a::attr(href)").extract()[-1] #'/products/page-23'
        last_page_num = int(last_page[ last_page.find("page-") + 5:])
        # print("last_page_num = {}".format(last_page_num))
        page = 1
        while page <= last_page_num:
            next_page = "https://store.special-learning.com/products/page-" + str (page)
            yield scrapy.Request(next_page, callback=self.parse)
            page += 1

    def parse_ceu (self, response):

        item = AbaCeusItem()
        ##
        item['crawl_date'] = get_datetime()
        ##
        item['title'] = response.css(".product_title.pull-left::text").extract()[0].strip()
        ##
        lst_temp = response.css(".description p::text , .description p strong::text").extract()
        if len(lst_temp) > 0:
            count = 0
            for j in lst_temp[:20]:
                if "LEVEL:" in j or "Level:" in j or "Eligibility" in j or "(BACB®)" in j or "(QABA®)" in j:
                    lst_temp.pop(count)
                    # count -= 1 if count != 0 else 0
                    count -= 1
                count += 1
            pos = 0
            for i in lst_temp[1:]:
                if '\xa0' == i:
                    break
                pos += 1
            lst_temp = lst_temp[:pos]    
            str_temp = ""
            
            
            item['description'] = str_temp.join(lst_temp).replace("\xa0","")     
        ##
        whole_des = response.css(".description p::text , .description p strong::text, .description ul li::text , .description ul li strong::text").extract()
        ##
        pos = 0
        flg_count = 0 
        for i in whole_des: 
            if "Date: " == i or "Original Date of Broadcast:" == i: 
                flg_count = 1
                break 
            pos += 1
        if flg_count == 1:    
            item['date_published']  = whole_des[pos + 1]
        else:
            item['date_published']  = None
        ##
        item['url'] = response.url
        ##
        try:
            item['image_url'] = response.css(".main_image img::attr(src)").extract()
        except:
            item['image_url'] = None
        ##
        try:
            item['price'] = response.css(".product_price .price_value:not(.old_price.price_value)::text").extract()[0].strip()
        except:
            item['price'] = None
        ##
        pos = 0
        flg_count = 0
        for i in whole_des:
            if "BACB®" in i: #(BACB®)
                new_temp = whole_des[pos].strip().split()
                if new_temp[0] == "(BACB®)":
                    flg_count = 1
                elif new_temp[0] == "BACB®":
                    flg_count = 2
                break
            elif "BACB CEU:" in i:
                flg_count = 3
                break
            elif "CEU:" in i:
                new_temp = whole_des[pos].strip().split()
                if new_temp[0] == "CEU:":
                    flg_count = 4
                elif "ASHA" in new_temp:
                    flg_count = 5
                break
            elif "CE Eligibility:" == i:
                flg_count = 6
                break
            else:
                pos += 1
        ##
        if flg_count == 1:
            temp = whole_des[pos].strip().split()
            item['ceu_credits'] = temp[1] if temp[1] != "-" else temp[2]
            count = 0
            for i in temp:
                if "Type" == i:
                    item['ceu_type'] = temp[count + 1]
                    break
                elif "Type-" in i:
                    item['ceu_type'] = temp[count][-2:]
                    break
                else:
                    pass
                count += 1    
        ##
        elif flg_count == 2:
            temp = whole_des[pos].strip().split()
            item['ceu_credits'] = temp[1] if temp[1] != "-" else temp[2]
            count = 0
            for i in temp:
                if "Type" == i:
                    item['ceu_type'] = temp[count + 1].replace(",","")
                    break
                elif "Type-" in i:
                    item['ceu_type'] = temp[count][-2:]
                    break
                else:
                    pass
                count += 1    
        
        ##
        elif flg_count == 3:
            temp = whole_des[pos].strip().split()
            item['ceu_credits'] = temp[2] if temp[2] != "-" else temp[3]
            count = 0
            for i in temp:
                if "Type" == i:
                    item['ceu_type'] = temp[count + 1]
                    break
                elif "Type-" in i:
                    item['ceu_type'] = temp[count][-2:]
                    break
                else:
                    pass
                count += 1
        
        ##
        elif flg_count == 4:
            temp = whole_des[pos].strip().split()
            item['ceu_credits'] = temp[1]
            count = 0
            for i in temp:
                if "Type" == i:
                    item['ceu_type'] = temp[count + 1].replace(",","")
                    break
                elif "Type-" in i:
                    item['ceu_type'] = temp[count][-3:].replace(")","").replace("-","")
                    break
                else:
                    pass
                count += 1
        ##
        elif flg_count == 5:
            temp = whole_des[pos].strip().split()
            item['ceu_credits'] = temp[2] if temp[2] != "-" else temp[3]
            count = 0
            for i in temp:
                if "Type" == i:
                    item['ceu_type'] = temp[count + 1]
                    break
                elif "Type-" in i:
                    item['ceu_type'] = temp[count][-2:]
                    break
                else:
                    pass
                count += 1    
        
        ##
        elif flg_count == 6:
            temp = whole_des[pos+1].strip().split()
            item['ceu_credits'] = temp[0] if temp[0] != "This" else None
            count = 0
            for i in temp:
                if "Type" == i:
                    item['ceu_type'] = temp[count + 1]
                    break
                elif "Type-" in i:
                    item['ceu_type'] = temp[count][-3:].replace(")","")
                    break
                else:
                    pass
                count += 1
        ##
        else:
            item['ceu_credits'] = None
            ##
            item['ceu_type'] = None        
        ##
        item['ceu_media_type'] = "Podcast"
        ##
        item['ceu_provider_slug'] = 'Special-Learning'
        ##
        yield(item)    
