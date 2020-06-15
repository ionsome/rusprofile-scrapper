#!/bin/python3

from scrapy.crawler import CrawlerProcess
from rusprofile_spider import RusprofileSpider


if __name__ == '__main__':
    settings = {
        'FEEDS': {
            'items.json': {'format': 'json'},
        },
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'RedWhite',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 1,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(RusprofileSpider, ids=[89220, 429110])
    process.start()
