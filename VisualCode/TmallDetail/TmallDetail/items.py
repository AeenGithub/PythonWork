# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmalldetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemid = scrapy.Field()
    brand_name= scrapy.Field()
    basic_contents = scrapy.Field()
    result_price = scrapy.Field()
    result_time = scrapy.Field()
