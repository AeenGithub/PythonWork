# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:51:59 2018

@author: S103878
"""

import csv
import json
import random
import time
from datetime import datetime

import pandas as pd
import requests


class Comments(object):
    def __init__(self,pathfile):
        self.pathfile = pathfile
        datenw = datetime.now().strftime('%Y%m%d%H%M')
        self.filename = '{}_{}.csv'.format(self.pathfile[10:15], datenw)
        self.conment_url = 'https://rate.tmall.com/list_detail_rate.htm'
        self.order = 3
        self.a = '1'
        self.get_file()
        self.columns = ['title', 'item_id', 'totalCount', 'comments']

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['title', 'item_id', 'totalCount', 'displayUserNick', 'comments']
        with open(self.filename,'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return 'ok'

    def get_url(self):
        '''通过已经有的宝贝链接文件，生成新的URL'''
        with open(self.pathfile, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield 'https:'+row['url']

    def set_resquests(self, url):
        one_item_comments = []
        thatid = url[-12:]
        datenum = int((datetime.now()-datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')).total_seconds()*1000)
        headers = { 'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(thatid)}
        get_url =  '''https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?\
jsv=2.4.8&appKey=12574478&t={0}&sign=c5aca960613336cd613ca34284\
6fb95a&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid\
=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjs\
onp2&data=%7B%22itemNumId%22%3A%22{1}%22%7D'''.format(datenum, thatid)
        s = requests.Session()
        s.get(url, headers=headers)
        res = s.get(get_url, headers=headers)
        time.sleep(5+random.random())
        json_data = json.loads(res.text[11:-1])
        title = json_data['data']['item']['title']
        commentcount = json_data['data']['item']['commentCount']
        userid = json_data['data']['seller']['userId']
        shopid = json_data['data']['seller']['shopId']
        comment_data = {
            'itemId': thatid,
            'sellerId': userid,
            'order': '3',
            'currentPage': self.a,
            'pageSize': '10',
            'callback': '_DLP_2535_der_3' + '_currentPage_' + self.a + '_pageSize_' + '10' + '_'
        }
        comment_req = s.get(self.conment_url, headers=headers, timeout=8, params=comment_data)
        comment_json = json.loads(comment_req.text[46:-1])
        last_page = comment_json['rateDetail']['paginator']['lastPage']
        print('宝贝', thatid, '一共有', last_page, '页评论')
        for i in range(1, last_page+1):
            print(thatid, i, '页的评论正在读取中')
            self.a = i
            comment_req = s.get(self.conment_url, headers=headers, timeout=8, params=comment_data)
            time.sleep(2 + random.random())
            comment_json = json.loads(comment_req.text[46:-1])
            comments = comment_json['rateDetail']['rateList']
            for one_comment in comments:
                rate_comment = one_comment['rateContent']
                displayUserNick = one_comment['displayUserNick']
                one_piece = [thatid, title, commentcount, displayUserNick, rate_comment]
                with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows([one_piece])
                one_item_comments.append(one_piece)
        print('宝贝', thatid, '数据保存完成')
        return one_item_comments

    def main(self):
        for one_url in self.get_url():
            print(one_url[-12:], 'is running, please waiting\n')
            try:
                s = self.set_resquests(one_url)
                comments = pd.DataFrame(s)
                date_only = datetime.now().strftime('%Y%m%d%H%M')
                comments.to_csv(r'I:\comments\{}_{}.csv'.format('only_comments', date_only), encoding='utf-8')
            except Exception as e:
                print(e)
                continue
        return '\nsuccessfully, 所有的数据都已经完全爬取成功!'


if __name__ == '__main__':
    pathfile = r"I:\Tmall\pb89_201808040025.csv"
    CM = Comments(pathfile)
    print(CM.main())
