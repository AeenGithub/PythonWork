# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniqlospideringItem(scrapy.Item):
    ageclss = scrapy.Field()
    junior_name = scrapy.Field()
    senior_name = scrapy.Field()
    senior_name_url = scrapy.Field()
    productName = scrapy.Field()
    ClassPicUrl = scrapy.Field()
    productCode = scrapy.Field()
    price = scrapy.Field()
    mainPic = scrapy.Field()
    label = scrapy.Field()

class UniqloJsonItem(scrapy.Item):
    path = scrapy.Field()
    tplt = scrapy.Field()
    backgroundFit = scrapy.Field()
    components = scrapy.Field()
    superCode = scrapy.Field()
    backgroundFixed = scrapy.Field()
    title = scrapy.Field()

class UniqlocategoriesItem(scrapy.Item):
    fexpand = scrapy.Field()
    fcode = scrapy.Field()
    fparentCode = scrapy.Field()
    fname = scrapy.Field()
    fsort = scrapy.Field()
    expand = scrapy.Field()
    code = scrapy.Field()
    parentCode = scrapy.Field()
    name = scrapy.Field()
    sort = scrapy.Field()

class UniqloDetailItem(scrapy.Item):
    productName = scrapy.Field()
    littlecode = scrapy.Field()
    sales = scrapy.Field()
    mainPic = scrapy.Field()
    season = scrapy.Field()
    originPrice = scrapy.Field()
    preSaleName = scrapy.Field()
    littlename = scrapy.Field()
    minPrice = scrapy.Field()
    sex = scrapy.Field()
    styleText = scrapy.Field()
    material = scrapy.Field()
    categoryCode = scrapy.Field()
    productCode = scrapy.Field()
    label = scrapy.Field()
    size = scrapy.Field()
    first_category_code = scrapy.Field()
    first_category_name = scrapy.Field()
    second_category_code = scrapy.Field()
    second_category_name = scrapy.Field()



