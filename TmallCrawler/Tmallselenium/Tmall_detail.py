# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:35:54 2018

@author: leshuangjiang
"""

import csv
import json
import logging
import os
import random
import time
from datetime import datetime

import requests


class Producs_detail(object):
    def __init__(self):
        self.pathfile = r"E:\Tmall\Tmall_shop_all.csv"
        self.datenw = datetime.now().strftime('%m%d')
        self.get_url()
        self.get_shop_lst()
        self.getlog()

    def getlog(self):
        '''通过使用logging包将程序运行出错的地方进行记录'''
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='F:\\爬虫日志\\Tmall_detail_get.log',
                            filemode='w')

    def make_file(self, shop, item_id, title):
        """创建一个含有标题的表格"""
        if os.listdir('D:\\宝贝详情') is True:
            print(':\\宝贝详情文件夹不为空')
            os.rmdir('D:\\宝贝详情')
            os.mkdir('D:\\宝贝详情')
        else:
            pass
        filename = ':\\宝贝详情\\{}_{}_{}.csv'.format(shop, item_id, self.datenw)
        if os.path.exists(filename):
            return filename
        else:
            with open(filename, 'w', newline='', encoding='gbk') as f:
                writer = csv.DictWriter(f, fieldnames=title)
                writer.writeheader()
            return filename

    def get_url(self):
        """通过给定的所有宝贝的列表获取宝贝id和宝贝的链接"""
        with open(self.pathfile, 'r', newline='', encoding='gbk') as f:
            for one in f.readlines():
                try:
                    shop_name = one.split(',')[0]
                    item_id = one.split(',')[1]
                    shop_detail_url = one.split(',')[8]
                except KeyError:
                    logging.info('{} has passed'.format(item_id))
                    shop_name = item_id = shop_detail_url = None
                    pass
                yield (shop_name, item_id, shop_detail_url)

    def set_resquests(self, url):
        '''通过requests获取一家店铺的宝贝详细信息'''
        thatid = url[-12:].strip(' ')
        datenum = int((datetime.now()-datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds()*1000)
        headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(thatid)
                }
        get_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=6298b3c5128b9220debf6963eb1d7873&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%22itemNumId%22%3A%22{1}%22'.format(datenum, thatid)
        with requests.Session() as s:
            s.get(url, headers=headers)
            res = s.get(get_url, headers=headers)
            time.sleep(random.random())
        return json.loads(res.text[11:-1])

    def basic_info(self, json_data, item_id):
        """对获取的数据进行规整"""
        title = []
        contents = []
        subtitle = json_data['data']['item']['subtitle']
        userId = json_data['data']['seller']['userId']
        shopId = json_data['data']['seller']['shopId']
        basic_info = json_data['data']['props']['groupProps'][0]['基本信息']   #列表包含字典
        basic_info.extend([{'subtitle': subtitle}, {'userId': userId}, {'shopId': shopId}])
        basic_info.insert(0, {'item_id': item_id})
        for one_title in basic_info:
            # print(one_title)
            title.extend(list(one_title.keys()))
            contents.extend(list(one_title.values()))
        basic_contents = [dict(zip(title, contents))]
        return title, basic_contents

    def get_sell_price(self, json_data):
        sell_counts = json.loads(json_data['data']['apiStack'][0]['value'])
        transmitPrice = sell_counts['price']['transmitPrice']['priceText']
        try:
            oprice = sell_counts['price']['extraPrices'][0]['priceText']
        except KeyError as e:
            oprice = ''
        try:
            sellCount = sell_counts['item']['sellCount']
        except KeyError:
            sellCount = ''
        try:
            sell_img = sell_counts['item']['videos'][0]['videoThumbnailURL']
        except Exception:
            sell_img = ''
        result = dict(zip(['transmitPrice', 'oprice', 'sellCount', 'sell_img'], [transmitPrice, oprice, sellCount, sell_img]))
        return result

    def get_time_count(self, json_data):
        sell_counts = json.loads(json_data['data']['apiStack'][0]['value'])
        try:
            startTime = sell_counts['vertical']['jhs']['startTime']
            endTime = sell_counts['vertical']['jhs']['endTime']
            soldCount = sell_counts['vertical']['jhs']['soldCount']
        except KeyError:
            startTime = endTime = soldCount = ''
        result = dict(zip(['startTime', 'endTime', 'soldCount'], [startTime, endTime, soldCount]))
        return result

    def main(self):
        '''通过循环访问宝贝列表'''
        for shop_tuple in self.get_url():
            shop = shop_tuple[0]
            item_id = shop_tuple[1].strip(' ')
            url = r'https://detail.m.tmall.com/item.htm?id={}'.format(item_id)
            print('{0} {1}正在访问中'.format(shop, item_id))
            try:
                json_data = self.set_resquests(url)
                title, basic_info = self.basic_info(json_data, item_id)
                # sell_price = self.get_sell_price(json_data)
                # sell_time = self.get_time_count(json_data)
                # print(basic_info)
                # basic_info[0].update(sell_price)
                # basic_info[0].update(sell_time)
                # title = basic_info[0].keys()
                filename = self.make_file(shop, item_id, title)
                with open(filename, 'a+', encoding='gbk') as f:
                    writer = csv.DictWriter(f, fieldnames=title)
                    writer.writerows(basic_info)
                    print('{0} {1}保存成功\n'.format(shop, item_id))
            except Exception as e:
                print(e)
                logging.info('{}没有成功'.format(item_id))
                print('{}没有成功'.format(item_id))
                # continue


if __name__ == '__main__':
    tm = Producs_detail()
    # tm.make_file()
    tm.main()
    # print(tm.get_url())
    # print(tm.get_url().__next__())
    # print('all is ok')

# def get_monsellcounts(self, json_data):
#     item_basic = json_data['data']['item']['subtitle']
#     return item_basic['title'], item_basic['commentCount'], item_basic



