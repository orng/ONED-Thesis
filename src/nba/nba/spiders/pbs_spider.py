#!/usr/bin/env

import sys
from datetime import datetime

import scrapy 
import regex as re
import dateutil.parser

from nba.items import NbaItem
sys.path.append('..')
from preprocessing import preprocess
sys.path.remove('..')


PAGE_LIMIT = 10
START_PAGE_NR = 1
BASE_URL = 'http://www.pbs.org/newshour/tag/vote-2016/page/{PAGE_NR}/'

class PbsSpider(scrapy.Spider):
    name='pbs'
    allowed_domains = ['pbs.org']
    start_urls = [BASE_URL.format(PAGE_NR=START_PAGE_NR),]

    def __init__(self):
        self.currentPage = START_PAGE_NR
        super(PbsSpider, self)

    def parse(self, response):
        lis = response.xpath('//ul[@class="post-list cf"]/li[@class="hasthumb cf"]')
        for li in lis:
            try:
                text = li.xpath('div/div[@class="content"]/p/text()').extract()
                text = " ".join(text)
                dateString = li.xpath('div/div[@class="meta"]/text()').extract()[0]
                url = li.xpath('div/div[@class="content"]/p/a/@href').extract()[0]

                date = dateutil.parser.parse(dateString)

                item = NbaItem()
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

