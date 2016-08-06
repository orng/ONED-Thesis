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


PAGE_LIMIT = 100
START_PAGE_NR = 1

class BritanniaSpider(scrapy.Spider):
    name='britannia'
    allowed_domains = ['britannia.com']
    start_urls = ['http://www.britannia.com/history/narprehist.html']

    def __init__(self):
        self.currentPage = START_PAGE_NR
        super(BritanniaSpider, self)

    def parse(self, response):
        try:
            textParagraphs =  response.xpath('//td[@class="bodycopy"]//node()[not(parent::a)]/text()[normalize-space()]').extract()
            text = " ".join(textParagraphs)

            item = ArticleItem()
            item['text'] = text
            item['url'] = response.url
            item['date'] = self.currentPage
            yield item
        except Exception as e:
            print e

        #dig deeper, get more pages:
        if self.currentPage < PAGE_LIMIT:
            self.currentPage = self.currentPage + 1
            nextPageUrls = response.xpath('//a[b/text()[contains(., "Part")]]/@href').extract()
            for nextPageUrl in nextPageUrls:
                nextPageUrl = response.urljoin(nextPageUrl)
                yield scrapy.Request(nextPageUrl, callback=self.parse)

