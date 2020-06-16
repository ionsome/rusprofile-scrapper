#!/bin/python3

import argparse
import sys
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rusprofile_spider import RusprofileSpider


def parse_args():
    parser = argparse.ArgumentParser(
        description='Более подробные настройки в setting.py',
    )
    parser.add_argument(
        metavar='id',
        nargs='+',
        dest='ids',
        type=int,
        help='один/несколько кодов ОКВЭД',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    process = CrawlerProcess(get_project_settings())
    process.crawl(RusprofileSpider, ids=args.ids)
    process.start()


if __name__ == '__main__':
    sys.exit(main())
