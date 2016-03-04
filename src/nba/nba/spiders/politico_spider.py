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


PAGE_LIMIT = 5
START_PAGE_NR = 1
BASE_URL = 'http://www.politico.com/news/2016-elections/{PAGE_NR}'

class PoliticoSpider(scrapy.Spider):
    name='politico'
    allowed_domains = ['politico.com']
    start_urls = [BASE_URL.format(PAGE_NR=START_PAGE_NR),]

    def __init__(self):
        self.currentPage = START_PAGE_NR
        super(PoliticoSpider, self)

    def parse(self, response):
        divs = response.xpath('//div[@class="story-text is-compact"]')
        for div in divs:
            try:
                text = div.xpath('descendant::p[not (@class)]/text()').extract()
                text = " ".join(text)
                dateString = div.xpath('descendant::time/attribute::datetime').extract()[0]
                url = div.xpath('descendant::p[@class="story-full"]/a/@href').extract()[0]

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

