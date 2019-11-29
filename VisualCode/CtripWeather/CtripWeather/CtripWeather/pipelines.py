# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from datetime import datetime
# from CtripWeatherIndex.items import CtripweatherItem

class CtripweatherPipeline(object):
    def __init__(self):
        datenum = datetime.now().strftime('%Y%m%d%H')
        data_title = [
            'prov_name',
            'city_name',
            'title',
            'now_temper',
            'low_temper',
            'high_temper',
            'weather',
            'wind',
            'index_name',
            'index_clss',
            'index_describe',
        ]
        self.ctrip_file = open('携程天气{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.primary_writer = csv.DictWriter(self.ctrip_file, fieldnames=data_title)
        self.primary_writer.writeheader()

    def process_item(self, item, spider):
        self.primary_writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.wangyi_file.close()