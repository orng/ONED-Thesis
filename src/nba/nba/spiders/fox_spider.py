#!/usr/bin/env

import scrapy 
import regex as re

from nba.items import NbaItem
import sys
sys.path.append('..')
from preprocessing import preprocess
sys.path.remove('..')


PAGE_LIMIT = 50
BASE_URL = 'http://www.foxsports.com/nba/news'

class FoxSpider(scrapy.Spider):
    name='fox'
    allowed_domains = ['foxsports.com']
    start_urls = [BASE_URL,]

    def __init__(self):
        self.currentPage = 0
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
        contentlist = response.xpath('//div[@class="flex-article-content content-body story-body"]//p/text()').extract()
        article = "".join(contentlist)
        words = preprocess(article)
        if words == []:
            return

        item = NbaItem()
        item['text'] = words
        item['url'] = response.url
        yield item

