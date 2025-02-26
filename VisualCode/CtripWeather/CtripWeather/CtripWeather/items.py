# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CtripweatherItem(scrapy.Item):
    # define the fields for your item here like:
    prov_name = scrapy.Field()
    city_name = scrapy.Field()
    title = scrapy.Field()
    now_temper = scrapy.Field()
    low_temper = scrapy.Field()
    high_temper = scrapy.Field()
    weather = scrapy.Field()
    wind = scrapy.Field()
    index_name = scrapy.Field()
    index_clss = scrapy.Field()
    index_describe = scrapy.Field()
