###########################################################################
## Author       : Abdelbaky Ahmed "Upwork Freelancer"
## Date         : 10-20-2020
## Email        : abdalbaky.ahmed@gmail.com
## Version      : V01
## Description  : Cedar Group Learning Site scrapping CEUs
###########################################################################
import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime

class  CedarGroupLearningSpider(scrapy.Spider):
    name = 'cedar_group_learning'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_urls = [
        'https://cedargrouplearning.com/ceu-videos-for-board-certified-behavior-analysts/'
        ]
    contentful_provider_entry_id = '2Dk1CnVZDRwsHEJPy7vhmP'

    def parse(self, response):
        links = response.css(".edd_download_title a::attr(href)").extract() 

        for link in links:   
            yield response.follow(link, self.parse_ceu)
        
    def parse_ceu (self, response):
        ignore_lst = [
            'If you have already purchased webcast please ',
            'Fee: $25.00\n',
            ' to access video.',
            'Following this webcast, participants will:',   "\t",
            '\xa0',     '\n\xa0',   '\n',   '\xa0\n',   '\t\xa0',   '\xa0\t',   '\n\xa0\n',     '\n \xa0\n', 
            'Abstract',
            'Within the interview, we will cover a wide range of topics, including, but not limited to:',
            'I hope you can join us, or listen later at your convenience.',
            '\nWithin this webcast, participants will learn, from Michael Cummings, M.D. and Michael Cameron, Ph.D., BCBA-D about:',
            '***All sales are final.', '\n***All sales are final.',
            '\nPlease contact ', ' for any questions or information regarding our presentation.'

        ]
        
        item = AbaCeusItem()

        item['crawl_date'] = get_datetime()

        item['title'] = response.css(".fl-post-title span::text").extract()[0]        


        lst_desc = response.css(".fl-post-content.clearfix div p::text").extract()
        for i in ignore_lst:
            pos = 0    
            for x in lst_desc:
                if str(i) == str(x) :
                    # print("yesssssss \n")
                    lst_desc.pop(pos)
                pos += 1
        res = ""
        res = res.join(lst_desc) 
        res = res.split()
        item['description'] = res
        # print("description: " + res.join(lst_desc) )
        
        item['url'] = response.url
        # # print("url: " + str(item['url']))

        try:
            # item['image_url'] =  response.css(".size-medium.wp-image-112.aligncenter::attr(src), .aligncenter.wp-image-322.size-medium::attr(src), .size-medium.wp-image-116.aligncenter::attr(src)").extract()[0] 
            item['image_url'] = response.css(".fl-post-content.clearfix div p img::attr(src)").exxtrat()[0]
        except:
            item['image_url'] = None
        # # print("IMAGE URL: {}".format(str(item['image_url'])))

        item['price'] = response.css(".edd-add-to-cart.button.green.edd-submit::attr(data-price)").extract()[0] 
        
        str_cred = ""
        lst_cred = response.css(".fl-post-content.clearfix div p::text").extract()[0:4]
        if "CEU" in lst_cred[0]:
            str_cred = lst_cred[0]
        elif "CEU"  in lst_cred[2]:
            str_cred = lst_cred[2]
        else:
            str_cred = response.css(".fl-post-content.clearfix div p strong::text").extract()[0]    
        
        if str_cred[7] == '.':
            item['ceu_credits'] = str_cred[6:9]
            item['ceu_type']    = str_cred[16]
        else :
             item['ceu_credits'] = str_cred[6]
             item['ceu_type']    = str_cred[14]

        item['ceu_media_type'] = "Podcast" # Set static as all podcasts

         

        item['ceu_provider_slug'] = "Cedar-Group-Learning"        

        yield(item)
