# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:51:59 2018

@author: Aeenf
"""

import json
import logging
import random
import time
from datetime import datetime
from urllib import request

import requests


class Taobao_producs(object):
    def __init__(self):
        self.lst_headers = [
            {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
             "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}]
        self.headers = random.choice(self.lst_headers)
        datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.filename = 'D:\\Tmall\\{}_{}.csv'.format(
            'store_of_Tmall', datenum)
        # self.get_file()
        self.savelog()

    def savelog(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='D:Tmall_sale_counts.log',
                            filemode='w')

    def get_one_url(self):
            """从文件获取需要爬取的url链接"""
            title_url = []
            url_file = r"D:\文档\天猫\临时需求\沈凯\20180929\男女装加单-全网TOP100\result4.csv"
            with open(url_file, 'r', encoding='utf-8') as f:
                one_line = f.read().split('\n')
                # print(one_line)
                for o in one_line:
                    title_url.append(o.split(','))
            return title_url

    def set_resquests(self, url):
        thatid = url[39:]
        datenum = int((datetime.now()-datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')).total_seconds()*1000)
        headers = { 'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(thatid)}
        get_url =  '''https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=c5aca960613336cd613ca342846fb95a&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%7B%22itemNumId%22%3A%22{1}%22%7D'''.format(datenum, thatid)
        print(thatid)
        with requests.Session() as s:
            s.get(url, headers=headers)
            res = s.get(get_url, headers=headers)
            time.sleep(random.random())
        json_data = json.loads(res.text[11:-1])['data']['item']
        return (thatid, json_data)

    def get_picture(self, tup):
        id_url, json_data = tup
        picture_url = 'https:' + json_data['images'][0]
        title = json_data['title']
        print('{}正在下载'.format(id_url))
        filename = 'D:\\图片\\image\\{}.jpg'.format(id_url)
        request.urlretrieve(picture_url,filename=filename)
        return '{}下载成功\n'.format(id_url)

    def main(self):
        for title_url in self.get_one_url():
            title, url = title_url
            print('{} 正在访问'.format(title))
            try:
                tuple_of_data = self.set_resquests(url)
                print(self.get_picture(tuple_of_data))
            except Exception as e:
                print(e)
                print('{}访问失败'.format(url[-12:]))
            continue


if __name__ == '__main__':
    Tao = Taobao_producs()
    print(Tao.main())
