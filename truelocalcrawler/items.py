# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TruelocalcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Company(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    category = scrapy.Field()
    link = scrapy.Field()
