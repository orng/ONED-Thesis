#!/usr/bin/env

import scrapy 
from nba.items import NbaItem
import sys
sys.path.append('..')
from preprocessing import preprocess
sys.path.remove('..')

BASE_URL = 'http://www.nba.com/news/news_archive.html' 

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
        if nextPage and self.page_nr < 2:
            self.page_nr = self.page_nr + 1
            nextPageUrl = response.urljoin(nextPage[0])
            yield scrapy.Request(nextPageUrl, callback=self.parse)


    def parse_article(self, response):
        contentlist = response.xpath('//section[@id="nbaArticleContent"]//p/text()').extract()
        article = "".join(contentlist)
        words = preprocess(article)
        if words == []:
            return
        item = NbaItem()
        item['text'] = words
        item['url'] = response.url
        yield item

