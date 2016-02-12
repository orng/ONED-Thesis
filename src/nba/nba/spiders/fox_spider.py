#!/usr/bin/env

import scrapy 
from nba.items import NbaItem
import regex as re

class FoxSpider(scrapy.Spider):
    name='fox'
    allowed_domains = ['foxsports.com']
    start_urls = ['http://foxsports.com/nba/news',
            ]
    def parse(self, response):
        for url in response.xpath('//a[@class="buzzer-title-link"]/@href').extract():
            """
            Grab all the articles on the page
            """
            subdomain = "foxsports.com/nba"
            regexpr = r'.+foxsports.com/.+/story.+'
            url = response.urljoin(url)
            regexmatch = re.match(regexpr, url)
            if regexmatch is not None:
                #only scrape nba links, not video stuff
                yield scrapy.Request(url, callback=self.parse_article)

        #dig deeper, get more pages:
        nextPageLinks = response.xpath('//a[@class="nextPagination"]/@href').extract()
        for link in nextPageLinks:
            nextPageUrl = response.urljoin(link)
            print nextPageUrl
            yield scrapy.Request(nextPageUrl, callback=self.parse)


    def parse_article(self, response):
        contentlist = response.xpath('//div[@class="flex-article-content content-body story-body"]/p/text()').extract()
        article = "".join(contentlist)
        item = NbaItem()
        item['text'] = article
        item['url'] = response.url
        yield item

