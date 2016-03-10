#!/usr/bin/env

import sys
from datetime import datetime

import scrapy 
import regex as re
import dateutil.parser

from articles.items import ArticleItem
sys.path.append('..')
from preprocessing import preprocess
sys.path.remove('..')


PAGE_LIMIT = 4
START_PAGE_NR = 1
BASE_URL = 'http://www.cbsnews.com/feature/election-2016/{PAGE_NR}/'

class CbsSpider(scrapy.Spider):
    name='cbs'
    allowed_domains = ['cbsnews.com']
    start_urls = [BASE_URL.format(PAGE_NR=START_PAGE_NR),]

    def __init__(self):
        self.currentPage = START_PAGE_NR
        super(CbsSpider, self)

    def parse(self, response):
        lis = response.xpath('//div[@class="listing-basic-lead"]//li[@class="item"]')
        for li in lis:
            try:
                text = li.xpath('descendant::p/text()').extract()
                text = " ".join(text)
                dateString = li.xpath('descendant::span[@class="date"]/text()').extract()[0]
                url = li.xpath('a/@href').extract()[0]

                date = dateutil.parser.parse(dateString)

                item = ArticleItem()
                item['text'] = text
                item['url'] = response.urljoin(url)
                item['date'] = date
                yield item
            except Exception as e:
                print e

        #dig deeper, get more pages:
        if self.currentPage < PAGE_LIMIT:
            self.currentPage = self.currentPage + 1
            nextPageUrl = BASE_URL.format(PAGE_NR=self.currentPage)
            yield scrapy.Request(nextPageUrl, callback=self.parse)

