# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YitiaocrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field().Field()
    one_category_title = scrapy.Field()
    one_category_id = scrapy.Field()
    one_category_bannerList = scrapy.Field()
    seconde_id = scrapy.Field()
    seconde_title = scrapy.Field()
    third_category_id = scrapy.Field()
    searchTitle = scrapy.Field()
    searchId = scrapy.Field()
    page_seq = scrapy.Field()
    link_Url = scrapy.Field()
    categoryLevel3Name = scrapy.Field()
    categoryLevel2Name = scrapy.Field()
    mainImageUrl = scrapy.Field()
    productName = scrapy.Field()
    productId = scrapy.Field()
    secondTitle = scrapy.Field()
    title = scrapy.Field()
    stock = scrapy.Field()
    price = scrapy.Field()
    tagPrice = scrapy.Field()
    vip_Price = scrapy.Field()
    totalCount = scrapy.Field()
    supplierName = scrapy.Field()
