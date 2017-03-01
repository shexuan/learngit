# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CollectbooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    TITLE=scrapy.Field()
    AUTHOR=scrapy.Field()
    SCORE=scrapy.Field()
