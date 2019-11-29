# -*- coding: utf-8 -*-

import csv
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pickle
from datetime import datetime


class XiaomiyoupinPipeline(object):
    def __init__(self):
        data_title = [
            'senior_class',
            'senior_id',
            'content',
            'product_name',
            'gid',
            'market_price',
            'order_overdue',
            'price_min',
            'sale_mode',
            'sale_count',
            'sale_fee',
            'summary',
            'url',
            'start_time',
            'Img800',
            'comment_tag',
            'create_time',
            'end_time',
            'one_size_pid',
            'one_size_saled',
            'one_size_inventory',
            'one_size_name'
        ]
        datenw = datetime.now().strftime('%y%m%d')
        self.youpin_file = open(f'youpin{datenw}.csv', 'w', encoding='gbk', errors='ignore')
        self.primary_writer = csv.DictWriter(self.youpin_file, fieldnames=data_title)
        self.primary_writer.writeheader()
        self.pickle_file = open(f'youpin{datenw}', 'wb+')

    def process_item(self, item, spider):
        self.primary_writer.writerow(item)
        self.pickle_file.write(pickle.dumps(item))
        return item

    def close_spider(self, spider):
        self.youpin_file.close()
        self.pickle_file.close()
