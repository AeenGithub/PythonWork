# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:51:59 2018

@author: Aeenf
"""
import collections
import json
import logging
import random
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
                'User-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(item_id),
                'cookie': 'na=o5VNFLBbw3ACAbStZ7Gsu/la; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; lid=%E9%A3%8E%E4%BA%91%E5%86%B3%E5%9C%B0%E8%B5%B7; enc=qfAybA1uwdkVDFhI6B3RUmuhD0OJ63E7t1OFw%2BDIuxJm4MpdeVK7RamT0BtYdG%2BdXY52HyBBi9mFfh%2BBVPHicg%3D%3D; OZ_1U_2061=vid=vbd93eb163238a.0&ctime=1545378404&ltime=1545378398; sm4=310100; uss=""; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=8fb34a4ade78d35a5956b011232f693e_1546947597041; _m_h5_tk_enc=db5c0e84c12b431620997ab4da0ca297; t=b8f11d27c630eed0a142e5137c3f5aba; uc3=vt3=F8dByRIpaOaVA7aj0mY%3D&id2=Uoe8iq%2F1cXOw4g%3D%3D&nk2=1CAm%2BTqNx%2FMopg%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; lgc=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; _tb_token_=74078ee9e3d5e; cookie2=1c38f6a35c452a2754aac9b126ddef64; l=aB7oNbSTyHOnwXDXCMa4Ascd5VCxROfPe0yC1MaLtTqm0_-b7RXy1jno-VwR2_hC5BOy_K-5F; isg=BNPTAZ8Vi85sMED3S4gnpgHRYlf32GltluOddoXwLvIPBPKmDVmym2lSOjLPpL9C',
        }
        return headers

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
        with open(self.filepath, encoding='utf-8') as f:
            for row in f.readlines():
                shopname_url[row.split('\t')[1]] = row.split('\t')[0]
        shopname_lst = set(shopname_url.values())
        return shopname_lst

    def get_requests(self, itemid):
        header = self.setheaders(itemid)
        datenum = int((datetime.now()-datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds()*1000)
        get_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=a3224659070435e70aa889e0b35bdc76&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp3&data=%22itemNumId%22%3A%22{1}%22'.format(datenum, itemid)
        with requests.Session() as s:
            s.get(header['Referer'], headers=header)
            res = s.get(get_url, headers=header, timeout=30)
            time.sleep(random.random()*5)
        return json.loads(res.text[11:-1])

    def basic_info(self, json_data, item_id):
        """对获取的数据进行规整"""
        # title = []
        contents = {}
        # 获取基本信息，商品详细介绍
        if json_data['data'].get('props'):
            if json_data['data']['props'].get('groupProps'):
                basic_info = json_data['data']['props']['groupProps'][0]['基本信息']   #列表包含字典
            else:
                basic_info = json_data['data']['props']['propsList'][0]['baseProps']  # 列表包含字典
            for one_dict in basic_info:
                for x, y in one_dict.items():
                    contents[x] = y
        if json_data['data'].get('item'):
            api_item = json_data['data']['item']
            try:
                moduleDescParams_f = api_item['moduleDescParams']['f']
                api_item.pop('moduleDescParams')
            except KeyError as e:
                print('\t', e)
                moduleDescParams_f = ''
            api_item.pop('exParams')
            api_item.pop('countMultiple')
            image_urls = api_item['images']
            image_url_str = ','.join(image_urls)
            api_item.update({'images': image_url_str})
            basic_info_df = pd.DataFrame(contents, index=[0])
            basic_info_df['itemId'] = str(item_id)
            api_item_df = pd.DataFrame(api_item, index=[0])
            result_df = pd.merge(basic_info_df, api_item_df, how='outer', on=['itemId'])
            result_df['moduleDescParams_f'] = moduleDescParams_f
            return result_df

    def get_sell_price(self, json_data):
        if json_data['data'].get('apiStack'):
            sell_counts = json.loads(json_data['data']['apiStack'][0]['value'])
            try:
                transmitPrice = sell_counts['price']['transmitPrice']['priceText']
            except Exception as e:
                transmitPrice = ''
            try:
                oprice = sell_counts['price']['extraPrices'][0]['priceText']
            except (KeyError,IndexError) as e:
                print('\t没有促销活动')
                oprice = ''
            try:
                sellCount = sell_counts['item']['sellCount']
            except KeyError as e:
                sellCount = ''
            if sell_counts['item']['videos']:
                sell_video = sell_counts['item']['videos'][0]['url']
            else:
                print('\t没有宣传视频')
                sell_video = ''
            try:
                item_id = sell_counts['item']['itemId']
            except KeyError as e:
                item_id = ''
                print(e, '获取视频链接时出现异常')
            result = dict(zip(['itemId', 'transmitPrice', 'oprice', 'sellCount', 'sell_video'], [item_id, transmitPrice, oprice, sellCount, sell_video]))
            result_df = pd.DataFrame(result, index=[0])
            return result_df

    def get_time_count(self, json_data):
        try:
            sell_counts = json.loads(json_data['data']['apiStack'][0]['value'])
            startTime = sell_counts['vertical']['jhs']['startTime']
            endTime = sell_counts['vertical']['jhs']['endTime']
            soldCount = sell_counts['vertical']['jhs']['soldCount']
        except KeyError:
            startTime = endTime = soldCount = ''
        result = dict(zip(['startTime', 'endTime', 'soldCount'], [startTime, endTime, soldCount]))
        return result

    def get_keywords(self, json_data):
        try:
            keywords = json_data['data']['rate']['keywords']
            keyword_count = ['-'.join([i['word'], i['count']]) for i in keywords]
            str_keyword = ','.join(keyword_count)
            return str_keyword
        except KeyError as e:
            print('\t', e, '没有关键词评语')
            return ''

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
                json_data = self.get_requests(one_itemid)
                # str_keywords = self.get_keywords(json_data)
                try:
                    basic_info = self.basic_info(json_data, one_itemid)
                    # info_result.append(basic_info)
                    # price_video = self.get_sell_price(json_data)
                    # if isinstance(basic_info, pd.DataFrame) and isinstance(price_video, pd.DataFrame):
                    #     last_df = pd.merge(basic_info, price_video,how='outer', on=['itemId'])
                    # elif isinstance(basic_info, pd.DataFrame):
                    #     last_df = basic_info
                    # elif isinstance(price_video, pd.DataFrame):
                    #     last_df = price_video
                    # else:
                    #     last_df = pd.DataFrame()
                    last_df = basic_info.copy()
                    # last_df['keywords'] = str_keywords
                    print('\t{} {} {}保存成功\n'.format(num, one_shopname, one_itemid))
                    info_result.append(last_df)
                # 创建一个以店铺为名字的csv文件,并返回文件名
                except Exception as e:
                    print(e)
                num += 1
                continue
            result_basic_info = pd.concat(info_result, sort=False, ignore_index=True)
            result_basic_info.to_excel('D:\\Python\\TmallCrawler\\file\\190504\\{}_{}.xlsx'.format(one_shopname, self.datenw))
            print('{}保存成功\n'.format(one_shopname))
        return 'all is over'

if __name__ == '__main__':
    pfile = "D:\\Python\\TmallCrawler\\ur_678"
    tm = DataSave(pfile)
    tm.main()

