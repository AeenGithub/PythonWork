# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from datetime import datetime

from WangyiYanxun.items import CommentItem, FirstLevelItem


class WangyiyanxunPipeline(object):
    def __init__(self):
        datenum = datetime.now().strftime('%Y%m%d%H')
        data_title = [
            'FirstTitle',
            'frontDesc',
            'category_id',
            'category_name',
            'superCategoryId',
            'colorNum',
            'counterPrice',
            'item_id',
            'primaryPicUrl',
            'name',
            'simpleDesc',
            'retailPrice',
            'sellVolume',
            'material',
            'style',
            'comment'
            ]
        self.wangyi_file = open('wangyi{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.primary_writer = csv.DictWriter(self.wangyi_file, fieldnames=data_title)
        self.primary_writer.writeheader()
        comment_structure = [
            'item_id',
            'frontUserName',
            'content',
            'createTime'
        ]
        self.wangyi_file_comment = open('wangyi_comment_{}.csv'.format(datenum), 'w', errors='ignore', newline='')
        self.comment_writer = csv.DictWriter(self.wangyi_file_comment, fieldnames=comment_structure)
        self.comment_writer.writeheader()

    def process_item(self, item, spider):
        if isinstance(item, FirstLevelItem):
            self.primary_writer.writerow(item)
            return item
        elif isinstance(item, CommentItem):
            self.comment_writer.writerow(item)
            return item

    def close_spider(self, spider):
        self.wangyi_file.close()
        self.wangyi_file_comment.close()
