# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeibeicrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    iid = scrapy.Field()
    buying_info = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    sale_num = scrapy.Field()
    price = scrapy.Field()
    origin_price = scrapy.Field()
    stock = scrapy.Field()
    CommentCount = scrapy.Field()
    default_praise_count = scrapy.Field()
    favorRate = scrapy.Field()
    tags = scrapy.Field()
    page = scrapy.Field()