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


PAGE_LIMIT = 2
BASE_URL = 'http://www.foxsports.com/nba/news'

class FoxSpider(scrapy.Spider):
    name='fox'
    allowed_domains = ['foxsports.com']
    start_urls = [BASE_URL,]

    def __init__(self):
        self.currentPage = 1
        super(FoxSpider, self)

    def parse(self, response):
        for url in response.xpath('//a[@class="buzzer-title-link"]/@href').extract():
            """
            Grab all the articles on the page
            """
            subdomain = "foxsports.com/nba"
            regexpr = r'.+foxsports.com/nba/story.+'
            url = response.urljoin(url)
            regexmatch = re.match(regexpr, url)
            if regexmatch is not None:
                #only scrape nba links, not video stuff
                yield scrapy.Request(url, callback=self.parse_article)

        #dig deeper, get more pages:
        if self.currentPage < PAGE_LIMIT:
            self.currentPage = self.currentPage + 1
            nextPageUrl = "{0}?pn={1}".format(BASE_URL,self.currentPage)
            yield scrapy.Request(nextPageUrl, callback=self.parse)


    def parse_article(self, response):
        contentlist = response.xpath('//div[@class="flex-article-content content-body story-body"]//*/text()').extract()
        if len(contentlist) > 2:
            article = "".join(contentlist[:3])
        else:
            article = "".join(contentlist)
        #words = preprocess(article)
        words = article
        if words == "":
        #if words == []:
            return

        #Get the date the article was posted
        posted = response.xpath('//time/text()').extract()
        for item in posted:
            try:
                date = dateutil.parser.parse(item)
            except ValueError:
                continue
        if date is None:
            date = datetime.now()
    

        item = NbaItem()
        item['text'] = words
        item['url'] = response.url
        item['date'] = date
        yield item

