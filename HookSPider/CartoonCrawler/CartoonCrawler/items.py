# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CartooncrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    curl = scrapy.Field()
    count = scrapy.Field()
    init_title = scrapy.Field()
    init_index = scrapy.Field()
    cindex = scrapy.Field()
    viewsign = scrapy.Field()
    viewsign_time = scrapy.Field()
    mid = scrapy.Field()
    cid = scrapy.Field()
    ikey = scrapy.Field()
    index = scrapy.Field()
    image_url = scrapy.Field()
    one_seq = scrapy.Field()
    img_path = scrapy.Field()
    img_url = scrapy.Field()
    # pass
