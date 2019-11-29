# -*- coding: utf-8 -*-

import csv
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime


class TmalldetailPipeline(object):
    def __init__(self):
        datenum = datetime.now().strftime('%Y%m%d%H')
        fieldname = [
            'itemid',
            'brand_name',
            'basic_contents',
            'result_price',
            'result_time'
        ]
        self.detail_file = open('.\\result\\detail_file_{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.Tmall_detail = csv.DictWriter(self.detail_file, fieldnames=fieldname)
        self.Tmall_detail.writeheader()

    def process_item(self, item, spider):
        self.Tmall_detail.writerow(item)
        return item

    def close_spider(self, spider):
        self.detail_file.close()
