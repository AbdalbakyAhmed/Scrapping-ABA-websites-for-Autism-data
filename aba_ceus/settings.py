# Scrapy settings for aba_ceus project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import os

BOT_NAME = 'aba_ceus'

SPIDER_MODULES = ['aba_ceus.spiders']
NEWSPIDER_MODULE = 'aba_ceus.spiders'

# FEED_EXPORT_FIELDS = ['title', 'description', 'url', 'image_url', 'price', 'ceu_credits', 'ceu_media_type', 'ceu_type']
FEED_EXPORT_FIELDS = ['title', 'description', 'date_published', 'event_published','ceu_provider_slug' ,'url', 'image_url', 'price', 'ceu_credits', 'ceu_media_type', 'ceu_type']

USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = random.choice(USER_AGENT_LIST)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'aba_ceus.middlewares.AbaCeusSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'aba_ceus.middlewares.AbaCeusDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'scrapy.pipelines.images.ImagesPipeline': 1,
#     'aba_ceus.pipelines.ContentfulPipeline': 10,
#     'aba_ceus.pipelines.S3PipelineCSV': 10
# }

# S3 PipelineCSV Config and Images AWS Config
# AWS_PROFILE = os.environ.get('AWS_PROFILE')
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# IMAGES_STORE = os.environ.get('IMAGES_STORE')
# IMAGES_STORE_S3_ACL = 'public-read'
# IMAGES_THUMBS = {
#     'product-img': (328, 320),
#     'product-img-modal': (315, 367)
# }
# MEDIA_ALLOW_REDIRECTS = True

# """ CONTENTFUL SETTINGS """
# CONTENTFUL_MANAGEMENT_API_TOKEN = os.environ.get('CONTENTFUL_MANAGEMENT_API_TOKEN')
# CONTENTFUL_SPACE_ID = os.environ.get('CONTENTFUL_SPACE_ID')
# CONTENTFUL_MANAGEMENT_CDN_API_TOKEN = os.environ.get('CONTENTFUL_MANAGEMENT_CDN_API_TOKEN') # Content Delivery API - access token
# CONTENTFUL_ENV_ID = os.environ.get('CONTENTFUL_ENV_ID')
# CONTENTFUL_CONTENT_TYPE_ID = os.environ.get('CONTENTFUL_CONTENT_TYPE_ID')
# CONTENTFUL_FORCE_UPDATE = True