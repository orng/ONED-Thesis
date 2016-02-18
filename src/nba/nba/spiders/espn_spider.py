#!/usr/bin/env

import scrapy 
from nba.items import NbaItem

import sys
sys.path.append('..')
from preprocessing import preprocess
sys.path.remove('..')

class EspnSpider(scrapy.Spider):
    name='espn'
    allowed_domains = ['espn.go.com']
    start_urls = ['http://espn.go.com/nba/',
            ]
    def parse(self, response):
        for url in response.xpath('//a[@class=" realStory"]/@href').extract():
            """
            Grab all the articles on the page
            """
            yield scrapy.Request(response.urljoin(url), callback=self.parse_article)

    def parse_article(self, response):
        contentlist = response.xpath('//div[@class="article-body"]//p/text()').extract()
        article = "".join(contentlist)
        words = preprocess(article)
        if words == []:
            #we don't want empty articles
            return

        item = NbaItem()
        item['text'] = words
        item['url'] = response.url
        yield item

