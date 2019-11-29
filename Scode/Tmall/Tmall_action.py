# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:51:59 2018

@author: Aeenf
"""

import csv
import json
import logging
import random
import re
import time
from datetime import datetime

import requests


class TM_producs(object):

    def __init__(self):
        self.lst_headers = [
            {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
             "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}]
        self.headers = random.choice(self.lst_headers)
        datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.filename = 'E:\\Tmall\\{}_{}.csv'.format(
            'store_of_Tmall', datenum)
        self.get_file()
        self.savelog()
        # self.url = r'https://mecity.m.tmall.com'
        self.url = r'https://me-city.m.tmall.com'

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['store_name', 'item_id', 'price', 'quantity', 'sold',
                 'title', 'titleUnderIconList', 'totalSoldQuantity', 'url', 'img']
        with open(self.filename, 'w', newline='', encoding='gbk') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return '表格创建成功'

    def savelog(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='E:Tmall_sale_counts.log',
                            filemode='w')

    def get_one_url(self):
        """从文件获取需要爬取的url链接"""
        url_file = r"E:\Tmall\Tmall_shop.csv"
        with open(url_file, 'r', encoding='gbk') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                yield (row['NAME'], row['URL'])

    def get_totalpage(self, url):
        '''提取总页码数'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&shop_cn=%E5%A4%8F%E5%95%86%E5%9C%BA%E5%90%8C%E6%AC%BE%E7%9B%B4%E9%99%8D&ascid=1385437139&scid=1385437139&p=1&page_size=12&from=h5&shop_id=60014692&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        # endurl = '/shop/shop_auction_search.do?sort=s&shop_cn=%E5%A4%8F%E5%95%86%E5%9C%BA%E6%AC%BE5%E6%8A%98%E8%B5%B7&ascid=1379562464&scid=1379562464&p=1&page_size=12&from=h5&shop_id=566813579&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        totalpage_url = url + endurl.format(num)
        html = requests.get(totalpage_url, headers=self.headers).text
        infos = re.findall(r'\(({.*})\)', html)[0]
        infos = json.loads(infos)
        totalpage = infos.get('total_page')
        log_info = '{}页商品数据信息已经获得'.format(totalpage)
        logging.info(log_info)
        return int(totalpage)

    def get_products(self, page, store_name, url):
        '''提取单页商品列表'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&p={}&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        pro_url = url + endurl.format(page, num)
        html = requests.get(pro_url, headers=self.headers, timeout=10).text
        infos = re.findall(r'\(({.*})\)', html)[0]
        infos = json.loads(infos)
        products = infos.get('items')
        # logging.info('{}的{}页产品清单获取成功'.format(store_name, page))
        title = ['store_name', 'item_id', 'price', 'quantity', 'sold',
                 'title', 'titleUnderIconList', 'totalSoldQuantity', 'url', 'img']
        with open(self.filename, 'a', newline='', encoding='gbk', errors='ignore') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writerows(products)
            lwriter = csv.writer(f)
            lwriter.writerows([[store_name]])

    def main(self):
        '''循环爬取所有页面宝贝'''
        # for i in self.get_one_url():
        store_url = self.url
        store_name = 'ME&CITY'
        print(store_name, '正在访问')
        try:
            total_page = self.get_totalpage(store_url)
        except TypeError as e:
            print(e, '获取总页面失败')
            logging.info(e)
            total_page = 1
        for i in range(1, total_page + 1):
            try:
                self.get_products(i, store_name, store_url)
                print('总计{}页商品，已经提取到{}页'.format(total_page, i))
                time.sleep(0.5 + random.random)
            except Exception as e:
                logging.info(e)
                pass
            continue
        logging.info(store_name)


if __name__ == '__main__':
    tm = TM_producs()
    tm.main()
