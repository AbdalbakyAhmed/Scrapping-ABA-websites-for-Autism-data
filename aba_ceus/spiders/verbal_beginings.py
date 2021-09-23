###########################################################################
## Author       : Abdelbaky Ahmed
## Date         : 10-19-2020
## Version      : V01
## Description  : Verbal Beginings Site scrapping CEUs
###########################################################################

import scrapy
from scrapy import Request
from aba_ceus.items import AbaCeusItem

from aba_ceus.utils import get_datetime

class VerbalBeginingsTrackSpider (scrapy.Spider):
    name = 'verbal_beginings_track'
    ## allowed_domains = ['https://www.verbalbeginnings.com']
    start_url = ['https://www.verbalbeginnings.com/vbu-online/']
    contentful_provider_entry_id = '4VTPetgrbbG3EoByVsWaM4'

    def parse(self, response):
        None