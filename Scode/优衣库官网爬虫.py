# coding: utf-8
'''
author: Aeenf
title: 获取优衣库官网上门店的分布和名称
'''

import json

import pandas as pd
import requests


class Uniqlo(object):
    def __init__(self):
        self.url = r'https://d.uniqlo.cn/hmall-store-service/i/site/queryAllstoreToJson/zh_CN'
        self.headers = {
            'User-Agent': 'Mozilla/5.0(Windows NT 6.2 Win64 64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Host': 'd.uniqlo.cn',
            'Connection': 'keep-alive',
            'Origin': 'https://www.uniqlo.cn',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Referer': 'https://www.uniqlo.cn/shop/shop_list.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

    def get_url(self):
        response_url = requests.get(self.url, headers=self.headers)
        response_url.encoding = 'utf-8'
        json_data = json.loads(response_url.text)
        resp = json_data['resp']
        return resp
        #soup_url.select('a[href]')

    def deal_with_url(self, lst):
        '''对下载的数据进行处理'''
        all_lst = []
        for i in lst:
            all_lst.append(i)
        df = pd.DataFrame(all_lst)
        df.to_excel('E:\\地址信息1225.xlsx')
        return 'ok'

if __name__ == '__main__':
    uniqlo = Uniqlo()
    lst = uniqlo.get_url()
    # print(lst[0])
    print(uniqlo.deal_with_url(lst))
