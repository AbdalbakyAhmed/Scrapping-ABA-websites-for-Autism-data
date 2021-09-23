# abanerd-scrapy


## AbaCeusItem

```python

    crawl_date = scrapy.Field() # Generate using from `aba_ceus.utils import get_datetime`
    date_published = scrapy.Field() # The date which the CEU was pulished
    event_date =  scrapy.Field() # (OPTIONAL) If the CEU is an event with a date of the event. 
    title = scrapy.Field() # Title from the CEU Entry being scraped
    description = scrapy.Field() # The description found on the page for the CEU.
    url = scrapy.Field() # The URL of the page where the CEU is found.
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    price = scrapy.Field() # The cost of the CEU in $USD
    ceu_credits = scrapy.Field() # float for CEU credits
    ceu_media_type = scrapy.Field() # A predetermine type of media.
    ceu_type = scrapy.Field() # This is a standard for this field and every CEU may be assocaited with one ore many of these. 
    image_full = scrapy.Field() # Full URL path of S3 link for the original image
    image_preview = scrapy.Field() # Full URL path to S3 link to 'product-img'
    image_modal = scrapy.Field() # Full URL path to S3 link to 'product-modal'

```


## Special Fields

These two fields only take the following strings as input. This validation is done at 

`ceu_media_type = ['Podcast', 'Live Online Course', 'Pre-Recorded Webinar', 'Live Webinar', 
'In-Person Training', 'Self Paced Online Course' ]`

`ceu_type = ['Type 1', 'Type 2', 'Type 3', 'Ethics', 'Supervision' ]`