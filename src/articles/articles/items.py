# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #title = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
