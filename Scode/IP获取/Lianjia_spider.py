# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 18:13:59 2018

@author: S103878
"""

import json

import requests
from bs4 import BeautifulSoup


class Lianjia_spider(object):
    def __init__(self):
        '''获取基础网址'''
        self.base_url = r'https://bj.lianjia.com/ershoufang/rs%E4%B8%9C%E5%9F%8E%E5%8C%BA/'
        self.data_list = []
    
    
    def get_data(self):
        '''get data from web'''
        data = requests.get(self.base_url).content.decode('utf-8')
        return data
    
    def parse_data(self, data):
        ''' parse data using re and bs4'''
        soup = BeautifulSoup(data, 'lxml')
        '''css 选择器 抽取数据验证 列表数组'''
        '''注意select中需要有一个点.'''
        data_list = soup.select('.sellListContent li')          #遍历一页数据 提取详细数据
        for li in data_list:
            '''li --> a --> img --alt'''
            '''using dict save data by key:value'''
            dict_data = {}
            if len(li.select('a img')) > 0:
                dict_data['room_name'] = li.select('a img')[0].get('alt')
            if len(li.select('.houseInfo a')) > 0:
                dict_data['houseinfo'] = li.select('.houseInfo a')[0].get_text()
            if len(li.select('.houseInfo')) > 0:
                dict_data['content'] = li.select('.houseInfo')[0].get_text()
            if len(li.select('.totalPrice')) > 0:
                dict_data['price'] = li.select('.totalPrice')[0].get_text()
            '''put one dict_data into a more big list'''
            self.data_list.append(dict_data)
                
    def save_data(self):
        '''save data using database'''
        data_str = json.dumps(self.data_list)
        with open(r'd:\\data.json', 'w') as f:
            f.write(data_str)
        return 'all data is ok'          
    
    def main(self):
        data = self.get_data()
        self.parse_data(data)
        print(self.save_data())

if __name__ == '__main__':
    Lianjia_spider().main()
