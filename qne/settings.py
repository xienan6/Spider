# -*- coding: utf-8 -*-

# Scrapy settings for vkspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
from scrapy.settings.default_settings import RANDOMIZE_DOWNLOAD_DELAY

BOT_NAME = 'xm_qunar_hotel'

SPIDER_MODULES = ['xm_qunar_hotel.spiders']
NEWSPIDER_MODULE = 'xm_qunar_hotel.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'vkspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'vkspider.middlewares.TutorialSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'vkspider.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'xm_qunar_hotel.rotate_userAgent.RotateUserAgentMiddleware': 400,
#    'scrapy.contrib.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
#    'vkspider.middlewares.ProxyMiddleWare': 125,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }


# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    # 'scrapy.pipelines.files.FilesPipeline': 1,
    # 'xm_qunar_hotel.pipelines.qunarSpiderPipeline': 300,  # 保存到mysql数据库
}

# FILES_STORE = 'F:\\Python code\\data\\Xm58\\files'
# FILES_URLS_FIELD = 'file_urls'
# FILES_RESULT_FIELD = 'files'
# FILES_EXPIRES = 30 #30天过期
#
# IMAGES_STORE = 'F:\\Python code\\data\\Xm58\\images'
# IMAGES_URLS_FIELD = 'cimage_urls'
# IMAGES_RESULT_FIELD = 'cimages'
# IMAGES_EXPIRES = 30 #30天过期
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPERROR_ALLOWED_CODES = [403]

LOG_LEVEL = 'INFO'
