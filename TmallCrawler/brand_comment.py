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
        self.filename = '{}_{}.csv'.format(self.pathfile[12:14], datenw)
        self.conment_url = 'https://rate.tmall.com/list_detail_rate.htm'
        self.order = 3
        self.a = '1'
        self.get_file()
        self.columns = ['title', 'item_id', 'totalCount', 'comments']

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['title', 'item_id', 'totalCount', 'comments']
        with open(self.filename,'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return 'ok'

    def get_url(self):
        '''通过已经有的宝贝链接文件，生成新的URL'''
        with open(self.pathfile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield 'https:'+row['url']

    def set_resquests(self, url):
        one_item_comments = []
        thatid = url[37:]
        datenum = int((datetime.now()-datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')).total_seconds()*1000)
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(thatid),
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9",
            'cookie': 'na=o5VNFLBbw3ACAbStZ7Gsu/la; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; lid=%E9%A3%8E%E4%BA%91%E5%86%B3%E5%9C%B0%E8%B5%B7; enc=qfAybA1uwdkVDFhI6B3RUmuhD0OJ63E7t1OFw%2BDIuxJm4MpdeVK7RamT0BtYdG%2BdXY52HyBBi9mFfh%2BBVPHicg%3D%3D; OZ_1U_2061=vid=vbd93eb163238a.0&ctime=1545378404&ltime=1545378398; sm4=310100; uss=""; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=8fb34a4ade78d35a5956b011232f693e_1546947597041; _m_h5_tk_enc=db5c0e84c12b431620997ab4da0ca297; t=b8f11d27c630eed0a142e5137c3f5aba; uc3=vt3=F8dByRIpaOaVA7aj0mY%3D&id2=Uoe8iq%2F1cXOw4g%3D%3D&nk2=1CAm%2BTqNx%2FMopg%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; lgc=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; _tb_token_=74078ee9e3d5e; cookie2=1c38f6a35c452a2754aac9b126ddef64; l=aB7oNbSTyHOnwXDXCMa4Ascd5VCxROfPe0yC1MaLtTqm0_-b7RXy1jno-VwR2_hC5BOy_K-5F; isg=BNPTAZ8Vi85sMED3S4gnpgHRYlf32GltluOddoXwLvIPBPKmDVmym2lSOjLPpL9C'
            }
        get_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=6298b3c5128b9220debf6963eb1d7873&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%22itemNumId%22%3A%22{1}%22'.format(datenum, thatid)
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
            'callback': '_DLP_2557_der_3' + '_currentPage_' + self.a + '_pageSize_' + '10' + '_'
        }
        # print(comment_data)
        comment_req = s.get(self.conment_url, headers=headers, timeout=8, params=comment_data)
        print(comment_req.text[47:-1])
        comment_json = json.loads(comment_req.text[47:-1])
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
                one_piece = [thatid, title, commentcount, rate_comment]
                with open(self.filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([one_piece])
                one_item_comments.append(one_piece)
        print('宝贝', thatid, '数据保存完成')
        return one_item_comments

    def main(self):
        for one_url in self.get_url():
            print(one_url[37:], 'is running, please waiting\n')
            s = self.set_resquests(one_url)
            comments = pd.DataFrame(s)
            date_only = datetime.now().strftime('%Y%m%d%H%M')
            comments.to_csv(r'D:\文档\家居与出行\comments\{}_{}.csv'.format('maojin_comments', date_only), encoding='utf-8')
        return '\nsuccessfully, 所有的数据都已经完全爬取成功!'


if __name__ == '__main__':
    pathfile = "D:\\文档\\家居与出行\\毛巾.csv"
    CM = Comments(pathfile)
    print(CM.main())
