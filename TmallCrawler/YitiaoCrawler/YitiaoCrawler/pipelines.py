# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json


class YitiaocrawlerPipeline(object):
    def open_spider(self, spider):
        title = {
            'one_category_title',
            'one_category_id',
            'one_category_bannerList',
            'seconde_id',
            'seconde_title',
            'third_category_id',
            'searchTitle',
            'searchId',
            'page_seq',
            'link_Url',
            'categoryLevel3Name',
            'categoryLevel2Name',
            'mainImageUrl',
            'productName',
            'productId',
            'secondTitle',
            'title',
            'stock',
            'price',
            'tagPrice',
            'vip_Price',
            'totalCount',
            'supplierName'
            }
        self.yitiao_file = open('yitiao.json', 'w', encoding='utf-8', errors='ignore')
        self.csv_file = open('yitiao.csv', 'w', encoding='gbk')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=title)
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        line_file = json.dumps(dict(item)) + "\n"
        with open('yitiao2.json', 'a+', encoding='utf-8') as f:
            line = json.dumps(dict(item)) + "\n"
            f.write(line)
        self.yitiao_file.write(line_file)
        self.csv_writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.yitiao_file.close()
        self.csv_file.close()
