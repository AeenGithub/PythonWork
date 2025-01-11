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
            {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}]
        self.headers = random.choice(self.lst_headers)
        self.headers['cookie'] = '''cna=o5VNFLBbw3ACAbStZ7Gsu/la; OZ_1U_2061=vid=vbc80bf5d21e62.0&ctime=1539836927&ltime=1539836926; sm4=310100; csa=undefined; t=d5cf7ba45b4ec8a1d0983bad48bee570; _tb_token_=7b9b4055b1d4d; cookie2=1fb9773bdff4bf3fa76ef019de38b5d3; _m_h5_tk=2821bd1b4432e16b5f0449235f9270cf_1540869175421; _m_h5_tk_enc=d42f94f58654299a5b4e642ee1a1f0e6; hng=""; uc1=cookie21=Vq8l%2BKCLjhS4UhJVbhgU&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=UoTYNk%2BmbVMk6w%3D%3D; uc3=vt3=F8dByRjP3P2FcttLjU4%3D&id2=Uoe8iq%2F1cXOw4g%3D%3D&nk2=1CAm%2BTqNx%2FMopg%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; tracknick=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; _l_g_=Ug%3D%3D; ck1=""; unb=1680414312; lgc=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; cookie1=WqH147gwEXHRwypXeqGsjnXlh76p%2FuypS0xDeyQ14Fs%3D; login=true; cookie17=Uoe8iq%2F1cXOw4g%3D%3D; _nk_=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; uss=""; csg=c8934b23; skt=a0083c70a71c8d80; enc=jLLPBVlpRXcNbWgnsoI5iYSO6GWaqeVV00ntQ%2BIJeQVuYMymyWIGBtn88mEr2JEY%2BeMutBiH7xcq7PMBJL4D%2Fw%3D%3D; x5sec=7b227477736d3b32223a223133626361356333363736386461353735653637346131356237613863326131434f4c7033743446454e616f6c616d6b6d7237344f686f4d4d5459344d4451784e444d784d6a7378227d; isg=BO_vsXYZ6LF5pOycBPuyuNdXfgPzxE2Rt9FmuwF8i95lUA9SCWTTBu1C1gBLKBsu'''
        datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.filename = 'D:\\Python\\TmallCrawler\\file\\{}_{}.csv'.format('store_of_Tmall', datenum)
        self.get_file()
        self.savelog()

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['store_name', 'item_id', 'price', 'quantity', 'sold',
                 'title', 'titleUnderIconList', 'totalSoldQuantity', 'url',
                 'img']
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

    def get_totalpage(self, url):
        '''提取总页码数'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&p=1&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        totalpage_url = url + endurl.format(num)
        html = requests.get(totalpage_url, headers=self.headers).text
        print(html)
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
        for shopname_url in self.get_one_url():
            store_name = shopname_url[0]
            print(store_name, '正在访问')
            store_url = shopname_url[1]
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
