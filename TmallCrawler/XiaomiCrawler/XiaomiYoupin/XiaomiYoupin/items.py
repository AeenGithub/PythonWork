# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaomiyoupinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    senior_class = scrapy.Field()
    senior_id = scrapy.Field()
    content = scrapy.Field()
    product_name = scrapy.Field()
    gid = scrapy.Field()
    market_price = scrapy.Field()
    order_overdue = scrapy.Field()
    price_min = scrapy.Field()
    sale_mode = scrapy.Field()
    sale_count = scrapy.Field()
    sale_fee = scrapy.Field()
    summary = scrapy.Field()
    url = scrapy.Field()
    start_time = scrapy.Field()
    Img800 = scrapy.Field()
    comment_tag = scrapy.Field()
    create_time = scrapy.Field()
    end_time = scrapy.Field()
    one_size_pid = scrapy.Field()
    one_size_saled = scrapy.Field()
    one_size_inventory = scrapy.Field()
    one_size_name = scrapy.Field()