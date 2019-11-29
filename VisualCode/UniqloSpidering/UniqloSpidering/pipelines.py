# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from datetime import datetime

from UniqloSpidering.items import UniqloDetailItem, UniqloJsonItem, UniqlocategoriesItem, UniqlospideringItem


class UniqlospideringPipeline(object):
    def __init__(self):
        datenum = datetime.now().strftime('%Y%m%d%H')
        home_fildnames = [
            'ageclss',
            'junior_name',
            'senior_name',
            'senior_name_url',
            'productName',
            'ClassPicUrl',
            'productCode',
            'price',
            'mainPic',
            'label'
            ]
        json_fildnames = [
            'path',
            'tplt',
            'backgroundFit',
            'components',
            'superCode',
            'backgroundFixed',
            'title'
        ]
        category_filednames = [
            'fexpand',
            'fcode',
            'fparentCode',
            'fname',
            'fsort',
            'expand',
            'code',
            'parentCode',
            'name',
            'sort'
        ]
        detail_filednames = [
            'first_category_code',
            'first_category_name',
            'second_category_code',
            'second_category_name',
            'productName',
            'littlecode',
            'sales',
            'mainPic',
            'season',
            'originPrice',
            'preSaleName',
            'littlename',
            'minPrice',
            'sex',
            'styleText',
            'material',
            'categoryCode',
            'productCode',
            'label',
            'size',
        ]
        self.Home_file = open('.\\result\\Home_file_{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.pages_file = open('.\\result\\Uniqlo_pages_{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.category_file = open('.\\result\\Uniqlo_categories_{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.detail_file = open('.\\result\\Uniqlo_detail_{}.csv'.format(datenum), 'w', encoding='gbk', errors='ignore', newline='')
        self.Uniqlo_home = csv.DictWriter(self.Home_file, fieldnames=home_fildnames)
        self.Uniqlo_home.writeheader()
        self.Uniqlo_detail = csv.DictWriter(self.detail_file, fieldnames=detail_filednames)
        self.Uniqlo_detail.writeheader()
        self.Uniqlo_pages = csv.DictWriter(self.pages_file, fieldnames=json_fildnames)
        self.Uniqlo_pages.writeheader()
        self.Uniqlo_categories = csv.DictWriter(self.category_file, fieldnames=category_filednames)
        self.Uniqlo_categories.writeheader()

    def process_item(self, item, spider):
        if isinstance(item, UniqloJsonItem):
            self.Uniqlo_pages.writerow(item)
            return item
        elif isinstance(item, UniqlospideringItem):
            self.Uniqlo_home.writerow(item)
            return item
        elif isinstance(item, UniqlocategoriesItem):
            self.Uniqlo_categories.writerow(item)
            return item
        elif isinstance(item, UniqloDetailItem):
            self.Uniqlo_detail.writerow(item)
            return item

    def close_spider(self, spider):
        self.pages_file.close()
        self.category_file.close()
        self.detail_file.close()
        self.Home_file.close()

