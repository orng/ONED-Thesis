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

BASE_URL = 'http://www.nba.com/news/news_archive.html' 
PAGE_LIMIT = 0

class NbaSpider(scrapy.Spider):
    name='nba'
    allowed_domains = ['nba.com']
    start_urls = [BASE_URL,]

    def __init__(self):
        super(NbaSpider, self)
        self.page_nr = 0

    def parse(self, response):
        for url in response.xpath('//div[@class="nbaNAContent"]//a/@href').extract():
            """
            Grab all the articles on the page
            """
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_article)

        #dig deeper, get more pages:
        nextPage = response.xpath('//a[contains(text(), "Previous Week")]/@href').extract()
        if nextPage and self.page_nr < PAGE_LIMIT:
            self.page_nr = self.page_nr + 1
            nextPageUrl = response.urljoin(nextPage[0])
            yield scrapy.Request(nextPageUrl, callback=self.parse)


    def parse_article(self, response):
        contentlist = response.xpath('//section[@id="nbaArticleContent"]//*/text()').extract()
        if len(contentlist) > 2:
            article = "".join(contentlist[:3])
        else:
            article = "".join(contentlist)
        #words = preprocess(article)
        words = article
        if words == []:
            return

        #Get the date the article was posted
        postedRegex = r'\w+ \d+, \d+ \d+:\d+ \w+'
        posted = response.xpath('//p[@class="nbaStoryDatePosted"]/text()').extract()
        try:
            dateString = re.search(postedRegex, posted[0])[0]
            date = dateutil.parser.parse(dateString)
        except (ValueError, IndexError):
            date = datetime.now()

        item = NbaItem()
        item['text'] = words
        item['url'] = response.url
        item['date'] = date
        yield item

