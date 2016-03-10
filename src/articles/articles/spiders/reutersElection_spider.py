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


PAGE_LIMIT = 10
START_PAGE_NR = 1
BASE_URL = 'http://www.reuters.com/news/archive/usElections?view=page&page={PAGE_NR}&pageSize=10'

class ReutersSpider(scrapy.Spider):
    name='reuters'
    allowed_domains = ['reuters.com']
    start_urls = [BASE_URL.format(PAGE_NR=START_PAGE_NR),]

    def __init__(self):
        self.currentPage = START_PAGE_NR
        super(ReutersSpider, self)

    def parse(self, response):
        divs = response.xpath('//div[contains(@class, "column1")]//div[@class="feature"]')
        for div in divs:
            try:
                url = div.xpath('h2/a/@href').extract()[0]
                text = div.xpath('p/text()').extract()[0]
                dateString = div.xpath('div[@class="relatedInfo"]/span/text()').extract()[0]

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

