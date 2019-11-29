# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 14:02:53 2018

@author: leshuangjiang
"""

import json
import os
import time
from datetime import datetime

import pandas as pd
import requests


class AmapCrwaler(object):
    def __init__(self):
        self.init_url = r'https://restapi.amap.com/v3/place/text?parameters'
        self.city_lst = "D:\\文档\\门店动态图\\city.csv"
        self.datenum = datetime.now().strftime('%Y%m%d%H')
        self.new_file_dir = 'd:\\经纬度\\{}'.format(self.datenum[:-2])
        if not os.path.exists(self.new_file_dir):
            os.mkdir(self.new_file_dir)

    def spiders(self, keywords, city):
        one_city_pois = []
        payload = {
            'key': '38223614c364192a208aa2bc3d4b2e74',
            'keywords': keywords,
            # 'types': '060000',
            'city': city,
            'citylimit': 'False',
            'offset': 20,
            'page': 1,
            'output': 'json'
        }
        result = requests.get(self.init_url, params=payload)
        json_data = json.loads(result.text)
        try:
            max_count = int(json_data['count']) // 20 + 1
            print('{}有{}条，{}页数据'.format(city, json_data['count'], max_count))
        except Exception:
            return ''
        for one_page in range(1, max_count + 1):
            print('\t第{}页正在检索中'.format(one_page))
            payload['page'] = one_page
            result = requests.get(self.init_url, params=payload)
            time.sleep(0.1)
            json_data_page = json.loads(result.text)
            pois = json_data_page['pois']
            one_city_pois.extend(pois)
        return one_city_pois

    def get_city_lst(self):
        with open(self.city_lst, encoding='utf-8') as f:
            reader = [one.split(',') for one in f.read().split('\n')]
        return reader[1:]

    def main(self, keyw):
        piece_of_city = []
        num = 0
        for city, adcode in self.get_city_lst():
            print('{}正在访问'.format(city))
            try:
                one_city_location = self.spiders(keyw, adcode)
                num = len(one_city_location) + num
                df_one_city_location = pd.DataFrame(one_city_location)
                piece_of_city.append(df_one_city_location)
            except Exception:
                pass
            print('截至一共有{}家, {}下载成功'.format(num, city))
        all_city_location = pd.concat(piece_of_city, sort=False, ignore_index=True)
        # all_city_location.to_csv('{}\\{}_{}.csv'.format(self.new_file_dir, self.datenum, keyw[:2], encoding='gbk', mode='a+'))
        all_city_location.to_csv('{}\\{}_{}.csv'.format(self.new_file_dir, self.datenum, keyw.replace('|', '_').replace(':', ''), encoding='gbk', mode='a+'))
        return 'all is ok, max_num is {}'.format(str(num))

    def all_brand(self):
        # brand_lst = ['热风|hotwind']
        brand_lst = ['美邦|美特斯邦威', '美特斯|邦威', 'meters bonwe|metersbonwe']
        for one_brand in brand_lst:
            print(one_brand)
            print(self.main(one_brand))
            print('\n*****************************\n')
        #         brand_lst = [
        #             '太平鸟', '以纯|yishion','江南布衣|JNBY', 'GXG|gxg',
        #     		'伊芙丽|eifini', '海澜之家|hlamall', 'GU', '美特斯邦威|metersbonwe',
        #             'UR', 'ONlY', '韩都衣舍', '拉夏贝尔|lachapelle', 'me&city', '杰克琼斯|jackjones', '阔色', '速写|croquis', 'lily|lilyfs',
        #             '播|broadcast', '欧时力|ochirly', '茵曼|inman', 'Aself|ruoji',
        #             'Material girl', 'trendiano', 'kon', 'lilbetter', 'viishow', 'jucy judy', '真维斯|jeanswest', '唐狮|tonlion', '爱居兔|Eichitoo',
        # '马克华菲', '佐丹奴', '卡宾', 'vero moda', 'Zara', 'H&M']
        # brand_lst = ['安踏|anta|小安踏', 'Lining|李宁', '热风', '阿迪|阿迪达斯|Adidas|AD KIDS', '耐克|Nike|NIKE KIDS',
        # '森马|semir|SEMIR', '海澜之家|Heilan|海澜', '乔丹', '以纯|Yishion|Teebox|Y:2', '利郎|LILANZ', '哥弟|GIRDEAR']
        else:
            return '所有的均已完成'


if __name__ == '__main__':
    amap = AmapCrwaler()
    # print(amap.get_city_lst())
    # amap.main()
    amap.all_brand()

# 'viishow', 'jucy judy', '真维斯|jeanswest', '唐狮|tonlion', '爱居兔|Eichitoo',
# '马克华菲', '佐丹奴', '卡宾', 'vero moda', 'Zara', 'H&M' - 首页官网