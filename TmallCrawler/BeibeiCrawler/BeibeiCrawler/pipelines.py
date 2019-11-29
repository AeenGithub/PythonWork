# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json


class BeibeicrawlerPipeline(object):
    def open_spider(self, spider):
        title = {
            'iid',
            'buying_info',
            'img',
            'title',
            'sale_num',
            'price',
            'origin_price',
            'stock',
            'CommentCount',
            'default_praise_count',
            'favorRate',
            'tags',
            'page'
        }
        self.csv_file = open('beibei.csv', 'w', encoding='gbk')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=title)
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        with open('beibei.json', 'a+', encoding='utf-8') as f:
            line = json.dumps(dict(item)) + "\n"
            f.write(line)
        self.csv_writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.csv_file.close()
