# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy

# ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1} # Commenting out as do not think it is required.

class AbaCeusItem(scrapy.Item):
    # define the fields for your item here like:
    crawl_date = scrapy.Field()
    
    date_published = scrapy.Field()
    event_published = scrapy.Field()
    
    title = scrapy.Field()
    description = scrapy.Field()
    
    url = scrapy.Field()
    
    image_url = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    
    price = scrapy.Field()
    
    ceu_credits = scrapy.Field()
    ceu_media_type = scrapy.Field()
    ceu_type = scrapy.Field()
    ceu_provider_slug = scrapy.Field()
    
    image_full = scrapy.Field() # Full URL path of S3 link for the original image
    image_preview = scrapy.Field() # Full URL path to S3 link to 'product-img'
    image_modal = scrapy.Field() # Full URL path to S3 link to 'product-modal'