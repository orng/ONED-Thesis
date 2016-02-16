#!/usr/bin/env

import scrapy 
from nba.items import NbaItem

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
        if not article.strip():
            return

        item = NbaItem()
        item['text'] = article
        item['url'] = response.url
        yield item

