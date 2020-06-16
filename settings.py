# default scrapy settings
# Find out more https://docs.scrapy.org/en/latest/topics/settings.html

ITEM_PIPELINES = {
    'scrapy_mysql_pipeline.MySQLPipeline': 301,
}

DOWNLOADER_MIDDLEWARES = {
    # replace user-agent logic
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # replace default retry
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 5
FEED_EXPORT_ENCODING = 'utf-8'


# MySQL pipeline settings
# Find out more https://github.com/IaroslavR/scrapy-mysql-pipeline
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'crawler'
MYSQL_PASSWORD = 'randompass'
MYSQL_DB = 'crawl'
MYSQL_TABLE = 'company'
MYSQL_UPSERT = True


# Connection
# User-Agents https://github.com/alecxe/scrapy-fake-useragent
RANDOM_UA_PER_PROXY = True

# Proxy https://github.com/TeamHG-Memex/scrapy-rotating-proxies
ROTATING_PROXY_LIST = []
if ROTATING_PROXY_LIST:
    DOWNLOADER_MIDDLEWARES.update(
        {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 310,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 320,
        })
