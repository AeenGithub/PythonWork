# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:51:59 2018

@author: Aeenf
"""
import collections
import json
import logging
import os
import random
import shutil
import time
from datetime import datetime

import pandas as pd
import requests


class DataSave(object):
    def __init__(self, pathfile):
        self.filepath = pathfile
        self.datenw = datetime.now().strftime('%m%d')
        self.get_log()

    def get_log(self):
        '''通过使用logging包将程序运行出错的地方进行记录'''
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='D:\\爬虫日志\\Tmall_detail_download.log',
                            filemode='w')

    def setheaders(self, item_id):
        headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(item_id)
                }
        return headers

    def make_file(self, shop, title):
        """创建一个含有标题的表格"""
        try:
            os.mkdir('D:\\宝贝详情')
        except Exception:
            print('文件夹已经存在')
        if os.listdir('D:\\宝贝详情'):
            print(':\\宝贝详情文件夹不为空')
            shutil.rmtree()('D:\\宝贝详情')
            os.mkdir('D:\\宝贝详情')
        else:
            pass
            
    def data_change(self, shop_name):
        '''从给定的文件里获取我想要的所有的URL'''
        shopname_url = collections.defaultdict()
        itemid_lst = []
        with open(self.filepath, encoding='utf-8') as f:
            for row in f.readlines():
                shopname_url[row.split('\t')[1]] = row.split('\t')[0]
        for one in shopname_url.items():
            if one[1] == shop_name:
                itemid_lst.append(one[0].strip('\n'))
        return itemid_lst

    def get_shop_name(self):
        shopname_url = collections.defaultdict()
        shopname_list = []
        with open(self.filepath, encoding='utf-8') as f:
            for row in f.readlines():
                shopname_url[row.split('\t')[1]] = row.split('\t')[0]
        shopname_lst = set(shopname_url.values())
        return shopname_lst

    def get_requests(self, itemid):
        header = self.setheaders(itemid)
        datenum = int((datetime.now()-datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds()*1000)
        get_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=6298b3c5128b9220debf6963eb1d7873&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%22itemNumId%22%3A%22{1}%22'.format(datenum, itemid)
        with requests.Session() as s:
            s.get(header['Referer'], headers=header)
            res = s.get(get_url, headers=header, timeout=30)
            time.sleep(random.random())
        return json.loads(res.text[11:-1])

    def basic_info(self, json_data, item_id):
        """对获取的数据进行规整"""
        title = []
        contents = []
        try:
            basic_info = json_data['data']['props']['groupProps'][0]['基本信息']   #列表包含字典
        except KeyError as e:
            print('{} props信息获取失败'.format(item_id))
            return None
        logging.info('{} props信息获取失败'.format(item_id))
        basic_info.insert(0, {'item_id': item_id})
        for one_title in basic_info:
            title.extend(list(one_title.keys()))
            contents.extend(list(one_title.values()))
        basic_contents = dict(zip(title, contents))
        return basic_contents

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

    def get_main_img(self, json_data):
        item_info = json_data['data']['item']
        images = item_info['images'][0]
        return {'images': images}

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
        # 获取所有的店铺列表
        for one_shopname in self.get_shop_name():
            # 通过传入一个店铺名称,获取他相关的宝贝id
            itemid_lst = self.data_change(one_shopname)
            print('{}共有{}个宝贝待访问'.format(one_shopname, len(itemid_lst)))
            info_result = []
            num = 1
            for one_itemid in itemid_lst:
                print('\t{} {} {}正在访问中'.format(num, one_shopname, one_itemid))
                # 对一个id进行访问,获取所有的相关信息
                try:
                    json_data = self.get_requests(one_itemid)
                    basic_info = self.basic_info(json_data, one_itemid)
                    main_img = self.get_main_img(json_data)
                    # print(sell_price)
                    print('\t{} {} {}保存成功\n'.format(num, one_shopname, one_itemid))
                    # 创建一个以店铺为名字的csv文件,并返回文件名
                    basic_info.update(main_img)
                    df_basic_info = pd.DataFrame(basic_info, index=range(2))
                    info_result.append(df_basic_info)
                    num += 1
                except Exception as e:
                    print(e)
                continue
            result_basic_info = pd.concat(info_result, ignore_index=True)
            result_basic_info.to_excel('D:\\Python\\{}_{}_2.xlsx'.format(one_shopname.replace('/',''), self.datenw))
            print('{}保存成功\n'.format(one_shopname))
        return 'all is over'

if __name__ == '__main__':
    pfile = r"D:\\Python\\TmallCrawler\\ur_678"
    tm = DataSave(pfile)
    tm.main()