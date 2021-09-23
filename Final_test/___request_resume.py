# ###########################################################################
# ## Author       : Abdelbaky Ahmed "Upwork Freelancer"
# ## Date         : 10-21-2020
# ## Email        : abdalbaky.ahmed@gmail.com
# ## Version      : V01
# ## Description  : Central Reach Site scrapping CEUs
# ###########################################################################
# import scrapy
# from scrapy import Request
# from aba_ceus.items import AbaCeusItem

# from aba_ceus.utils import get_datetime
# import json

# class  CentralReachSpider(scrapy.Spider):
#     name = 'central_reach'
#     ## allowed_domains = ['https://www.verbalbeginnings.com']
#     start_urls = [
#         'https://institute.centralreach.com/learn/browse?layoutId=4d408d11-9ca0-453b-b2a4-01954a56c9b9&widgetId=jduafq8&page=0'
#         ]
#     contentful_provider_entry_id = '1L1oN6s2WuZ2MdLfdsaIR3'

#     def parse(self, response):
#         JSON = json.loads(response.body)
#         #yield {'url':response.url}
#         for pre_item in JSON['contentItems']:
#             item = AbaCeusItem()
#             ##
#             item['crawl_date'] = get_datetime()
#             ##
#             try:
#                 item ['date_published']     = pre_item ['publishDate']
#             except:
#                 item ['date_published']     = None
#             ##
#             try:
#                 item ['event_published']    = pre_item ['courseStartDate']
#             except:
#                 item ['date_published']     = None
#             ##
#             item['title'] = pre_item['title']
#             ##
#             item['description'] = pre_item['description']     
#             ##
#             item['url'] = "https://institute.centralreach.com/courses/" + str(pre_item['slug'])
#             ##
#             item['image_url'] = pre_item['asset']
#             ##
#             try:
#                 item['price'] = pre_item['priceInCents']
#             except:
#                 item['price'] = 'Free'
#             ##
#             item['ceu_media_type'] = "Podcast"
#             ##
#             str_cred = pre_item['description']
#             if "II BACB" in str_cred:
#                 pos = int( str_cred.find("II BACB") )
#                 item['ceu_type']    = str_cred [ pos : pos + 2]
#                 item['ceu_credits'] = str_cred [pos - 7]
#             elif "Learning BACB" in str_cred:
#                 pos = int (str_cred.find("Learning BACB"))
#                 item['ceu_type']    = None
#                 item['ceu_credits'] = str_cred [pos - 2]
#             elif "II Ethics" in str_cred:
#                 pos = int (str_cred.find("II Ethics"))
#                 item['ceu_type']    = str_cred[pos : pos + 2 ]
#                 item['ceu_credits'] = str_cred [pos - 7 ]
#             elif "BACB Ethics" in str_cred :
#                 pos = int (str_cred.find("BACB Ethics"))
#                 item['ceu_type']    = None
#                 item['ceu_credits'] = str_cred [pos - 2 ]
#             else:
#                 item['ceu_type']    = None
#                 item['ceu_credits'] = None
#             ##
#             item['ceu_provider_slug'] = 'Central_Reach'
#             ##
#             yield item
        
#         if JSON['meta']['hasMore']==True:
#             next_url = 'https://institute.centralreach.com/learn/browse?layoutId=4d408d11-9ca0-453b-b2a4-01954a56c9b9&widgetId=jduafq8&page=' + str(int(response.url.split("page=")[-1])+1)
#             yield scrapy.Request(next_url , callback=self.parse)

