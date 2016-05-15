#!/usr/bin/env python

from datetime import datetime

import scrapy 
import regex as re
import dateutil.parser

from articles.items import ArticleItem


PAGE_LIMIT = 10
START_PAGE_NR = 1
BASE_URL = 'http://www.reuters.com/news/archive/topNews?view=page'
#BASE_URL = 'http://www.reuters.com/news/archive/usElections?view=page&page={PAGE_NR}&pageSize=10'

class ReutersNewsSpider(scrapy.Spider):
    name='reutersNews'
    allowed_domains = ['reuters.com']
    start_urls = [BASE_URL]

    def parse(self, response):
        urls = response.xpath('//h3[@class="story-title"]/a/@href').extract()
        for url in urls:
            articleUrl = response.urljoin(url)
            yield scrapy.Request(articleUrl, callback=self.parseArticle)

        nextUrl = response.xpath('//a[@class="control-nav-next"]/@href').extract_first()
        nextUrl = response.urljoin(nextUrl)
        yield scrapy.Request(nextUrl, callback=self.parse)

    def parseArticle(self, response):
        try:
            paragraphs = response.xpath('//span[@id="articleText"]//p/text()').extract()
            text = " ".join(paragraphs)
            title = response.xpath('//h1[@class="article-headline"]/text()').extract_first()
            timestamp = response.xpath('//span[@class="timestamp"]/text()').extract_first()

            item = ArticleItem()
            item['text'] = text
            item['url'] = response.url
            item['date'] = dateutil.parser.parse(timestamp)
            item['title'] = title 
            yield item

        except Exception as e:
            print e
        

