# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:51:59 2018

@author: S103878
"""

import csv
import json
import logging
import random
import time
from datetime import datetime

import pandas as pd
import requests


class Comments(object):
    def __init__(self, thatid, sellerid):
        # self.pathfile = pathfile
        # datenw = datetime.now().strftime('%Y%m%d%H%M')
        # self.filename = '{}_{}.csv'.format('I:\\comments\\taipingniao', datenw)
        self.comment_url = 'https://rate.tmall.com/list_detail_rate.htm'
        self.thatid = thatid
        self.userid = sellerid
        self.filename = '{}_{}.csv'.format(
            'I:\\comments\\mgirl', self.thatid)
        self.a = '1'
        self.columns = ['item_id', 'displayUserNick', 'auctionSku', 'comments']
        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        self.get_file()
        self.savelog()
    
    def savelog(self):
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='I:myapp.log',
                filemode='w')

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['item_id', 'displayUserNick', 'auctionSku', 'comments']
        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return 'ok'

    def set_resquests(self):
        one_item_comments = []
        comment_data = {
            'itemId': self.thatid,
            'sellerId': self.userid,
            'order': '3',
            'currentPage': '1',
            'pageSize': '10',
            'callback': '_DLP_2535_der_3' + '_currentPage_' + self.a + '_pageSize_' + '10' + '_'
        }
        s = requests.Session()
        comment_req = s.get(self.comment_url, headers=self.headers, params=comment_data)
        time.sleep(random.random() + 1)
        comment_json = json.loads(comment_req.text[46:-1])
        last_page = comment_json['rateDetail']['paginator']['lastPage']
        print('宝贝', self.thatid, '一共有', last_page, '页评论')
        for i in range(1, last_page+1):
            print(self.thatid, i, '页的评论正在读取中')
            comment_data = {
                'itemId': self.thatid,
                'sellerId': self.userid,
                'order': '3',
                'currentPage': '21',
                'pageSize': '10',
                'callback': '_DLP_2535_der_3' + '_currentPage_' + self.a + '_pageSize_' + '10' + '_'
            }
            time.sleep(2 + random.random())
            try:
                comment_req = s.get(
                    self.comment_url, headers=self.headers, params=comment_data)
                comment_json = json.loads(comment_req.text[46:-1])
                comments = comment_json['rateDetail']['rateList']
                print(comment_req.text[46:80])
                logging.info('This is info message')
                print('comments is over and saving\n')
                for one_comment in comments:
                    rate_comment = one_comment['rateContent']
                    displayUserNick = one_comment['displayUserNick']
                    auctionSku = one_comment['auctionSku']
                    one_piece = [thatid, displayUserNick,
                                 auctionSku, rate_comment]
                    with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerows([one_piece])
                    one_item_comments.append(one_piece)
            except ValueError as e:
                print(e)
                print('there is something wrong')
        print('宝贝', thatid, '数据保存完成')
        return one_item_comments

    def main(self):
        # for one_url in self.get_url():
        print(self.thatid, 'is running, please waiting\n')
        s = self.set_resquests()
        comments = pd.DataFrame(s)
        date_only = datetime.now().strftime('%Y%m%d%H%M')
        comments.to_csv(r'I:\comments\{}_{}.csv'.format(
            'mgirl_comments', self.thatid), encoding='utf-8', index=False)
        return '\nsuccessfully, 所有的数据都已经完全爬取成功!'


if __name__ == '__main__':
    # pathfile = r"I:\Tmall\pb89_201808040025.csv"
    # lst_id_tpn = ['564181756698', '564327998995', '562549558354', '555991866169', '573048394028']
    lst_id_mg = ['554476819330'] #'569640344307', '568017049823', '571442439366', '561877658672', '553293058164', 
    for i in lst_id_mg:
        thatid = i
        sellerid = '2002445600'
        CM = Comments(thatid, sellerid)
        print(CM.main())

# 564322042870 is over
# 564181756698 is over
# 564327998995 is over
# 562549558354 is over
# 555991866169
# 573048394028
# M  2002445600
# 569640344307
# 568017049823
# 571442439366
# 561877658672
# 553293058164
# 554476819330
