# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.item.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.item.Field()
    link = scrapy.item.Field()
    desc = scrapy.item.Field()
