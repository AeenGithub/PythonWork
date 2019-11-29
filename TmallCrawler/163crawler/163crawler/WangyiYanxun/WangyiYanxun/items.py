# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiyanxunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field() scrapy.Field()
    pass


class FirstLevelItem(scrapy.Item):
    FirstTitle = scrapy.Field()
    frontDesc = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    superCategoryId = scrapy.Field()
    colorNum = scrapy.Field()
    counterPrice = scrapy.Field()
    item_id = scrapy.Field()
    primaryPicUrl = scrapy.Field()
    name = scrapy.Field()
    simpleDesc = scrapy.Field()
    retailPrice = scrapy.Field()
    sellVolume = scrapy.Field()
    material = scrapy.Field()
    style = scrapy.Field()
    comment = scrapy.Field()


class CommentItem(scrapy.Item):
    item_id = scrapy.Field()
    frontUserName = scrapy.Field()
    content = scrapy.Field()
    createTime = scrapy.Field()