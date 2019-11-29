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
        # self.headers = self.set_headers()
        datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.filename = 'D:\\Python\\TmallCrawler\\file\\{}_{}.csv'.format('1_store_of_Tmall', datenum)
        self.get_file()
        self.savelog()

    def set_headers(self, **kwargs):
        init_headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN, zh; q=0.9",
            'cache-control': 'no-cache',
            }
        init_headers.update(kwargs)
        return init_headers

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['store_name', 'item_id', 'price', 'quantity', 'sold',
                 'title', 'titleUnderIconList', 'totalSoldQuantity', 'url',
                 'img', 'page']
        with open(self.filename, 'w', newline='', encoding='gbk') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return '表格创建成功'

    def savelog(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='D:\\Python\\TmallCrawler\\log\\Tmall_sale_counts.log',
                            filemode='w')

    def get_one_url(self):
        """从文件获取需要爬取的url链接"""
        url_file = r"D:\Python\TmallCrawler\file\Tamll_shop_all"
        with open(url_file, 'r', encoding='utf-8') as f:
            csv_reader = f.read().split('\n')
            for row in csv_reader:
                yield row.split('\t')

    def get_totalpage(self, url, doheader):
        '''提取总页码数'''
        num = random.randint(4012748, 85727482)
        endurl = '/shop/shop_auction_search.do?sort=s&p=1&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        totalpage_url = url + endurl.format(num)
        html = requests.get(totalpage_url, headers=doheader).text
        infos = re.findall(r'\(({.*})\)', html)[0]
        infos = json.loads(infos)
        totalpage = infos.get('total_page')
        log_info = '{}页商品数据信息已经获得'.format(totalpage)
        logging.info(log_info)
        return int(totalpage)

    def get_products(self, page, doheader, store_name, url):
        '''提取单页商品列表'''
        num = random.randint(10127482, 75727482)
        endurl = '/shop/shop_auction_search.do?sort=s&p={}&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        pro_url = url + endurl.format(page, num)
        # print(pro_url)
        html = requests.get(pro_url, headers=doheader, timeout=10).text
        # print(html[:100])
        infos = re.findall(r'\(({.*})\)', html)[0]
        infos = json.loads(infos)
        products = infos.get('items')
        for one_item in products:
            one_item['store_name'] = store_name
            one_item['page'] = page
        # 针对上一版本出现的首列出现空格，需要自己手动处理的问题
        # logging.info('{}的{}页产品清单获取成功'.format(store_name, page))
        title = ['store_name', 'item_id', 'price', 'quantity', 'sold',
                 'title', 'titleUnderIconList', 'totalSoldQuantity', 'url', 'img', 'page']
        with open(self.filename, 'a', newline='', encoding='gbk', errors='ignore') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writerows(products)        

    def main(self):
        '''循环爬取所有页面宝贝'''
        # for shopname_url in [('veromoda','https://veromoda.m.tmall.com/')]:
        for shopname_url in self.get_one_url():
            store_name = shopname_url[0]
            print(store_name, '正在访问')
            store_url = shopname_url[1]
            doheader = self.set_headers()
            doheader['referer'] = store_url + '/shop/shop_auction_search.htm?sort=default'
            try:
                total_page = self.get_totalpage(store_url, doheader)
            except Exception as e:
                print(e, '获取总页面失败')
                logging.info(e)
                total_page = 1
            for i in range(1, total_page + 1):
                print('总计{}页商品，正在访问第{}页'.format(total_page, i))
                try:
                    self.get_products(i, doheader, store_name, store_url)
                    print('总计{}页商品，已经提取到{}页\n'.format(total_page, i))
                    time.sleep(1 + random.random())
                except (IndexError, TypeError) as e:
                    logging.info(e)
                    pass
                continue
        logging.info(store_name)


if __name__ == '__main__':
    tm = TM_producs()
    tm.main()
    # print(tm.headers)
    print('所有的都已经运行结束')
