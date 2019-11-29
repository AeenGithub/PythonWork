import csv
import json
import os
import random
import time

import pandas as pd
import requests


class tmall_pinglun(object):
    def __init__(self, path):
        self.path = path
        self.base_dir = os.getcwd()

    def get_proxy(self):
        try:
            response = requests.get('http://localhost:5555/random')
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def get_itemid_pages(self, one_row):
        item_id = one_row[4]
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=430490406&order=3&currentPage=1&pageSize=10&&callback=_DLP_2586_der_3_currentPage_1_pageSize_10_'.format(
            item_id)
        headers = {
            'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(item_id),
            'cookie': 'cna=qMU/EQh0JGoCAW5QEUJ1/zZm; enc=DUb9Egln3%2Fi4NrDfzfMsGHcMim6HWdN%2Bb4ljtnJs6MOO3H3xZsVcAs0nFao0I2uau%2FbmB031ZJRvrul7DmICSw%3D%3D; lid=%E5%90%91%E6%97%A5%E8%91%B5%E7%9B%9B%E5%BC%80%E7%9A%84%E5%A4%8F%E5%A4%A9941020; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; x=__ll%3D-1%26_ato%3D0; t=2c579f9538646ca269e2128bced5672a; _m_h5_tk=86d64a702eea3035e5d5a6024012bd40_1551170172203; _m_h5_tk_enc=c10fd504aded0dc94f111b0e77781314; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ5bI3949Xhg%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEzZ1MVSremcx%2BQ%3D&id2=UNcPuUTqrGd03w%3D%3D&nk2=F5RAQ19thpZO8A%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=tb51552614; _l_g_=Ug%3D%3D; ck1=""; unb=3778730506; lgc=tb51552614; cookie1=UUBZRT7oNe6%2BVDtyYKPVM4xfPcfYgF87KLfWMNP70Sc%3D; login=true; cookie17=UNcPuUTqrGd03w%3D%3D; cookie2=1843a4afaaa91d93ab0ab37c3b769be9; _nk_=tb51552614; uss=""; csg=b1ecc171; skt=503cb41f4134d19c; _tb_token_=e13935353f76e; x5sec=7b22726174656d616e616765723b32223a22393031623565643538663331616465613937336130636238633935313935363043493362302b4d46454e76646c7243692b34364c54426f4d4d7a63334f44637a4d4455774e6a7378227d; l=bBIHrB-nvFBuM0pFBOCNVQhjb_QOSIRYjuSJco3Wi_5Bp1T1Zv7OlzBs4e96Vj5R_xYB4KzBhYe9-etui; isg=BDY2WCV-dvURoAZdBw3uwj0Oh2yUQwE5YzQQ9qAfIpm149Z9COfKoZwV-_8q0HKp',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'}
        data = {'itemId': item_id,
                'sellerId': 430490406,
                'order': 3,
                'currentPage': 1,
                'pageSize': 10,
                'callback': '_DLP_2586_der_3_currentPage_1_pageSize_10_'}

        res = requests.get(url=url, headers=headers, params=json.dumps(data))
        res_json = json.loads(res.text[res.text.find('{'):-1])
        pages = res_json.get('rateDetail').get('paginator').get('lastPage')
        one_row.append(pages)
        for page in range(1, int(pages) + 1):
            one_row_page = one_row + [page]
            with open(r'{}\semir_pages.csv'.format(self.base_dir), mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(one_row_page)
        print('商品ID:{} 评论总页数：{} 保存完毕'.format(item_id, pages))
        return ''

    def get_itemid_comment(self, one_row):
        new_one_row = one_row
        page = int(one_row[-1])
        item_id = one_row[4]
        if page != 0:
            print('-----------------------------------------------------')
            print('标题:{} ID：{} 总页数：{} 当前页数:{} 正在访问'.format(one_row[2], item_id, one_row[-2], page))
            url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=430490406&order=3&currentPage={}&pageSize=10&&callback=_DLP_2586_der_3_currentPage_{}_pageSize_10_'.format(
                item_id, page, page)
            headers = {
                'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(item_id),
                'cookie': 'cna=qMU/EQh0JGoCAW5QEUJ1/zZm; enc=DUb9Egln3%2Fi4NrDfzfMsGHcMim6HWdN%2Bb4ljtnJs6MOO3H3xZsVcAs0nFao0I2uau%2FbmB031ZJRvrul7DmICSw%3D%3D; lid=%E5%90%91%E6%97%A5%E8%91%B5%E7%9B%9B%E5%BC%80%E7%9A%84%E5%A4%8F%E5%A4%A9941020; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; x=__ll%3D-1%26_ato%3D0; t=2c579f9538646ca269e2128bced5672a; _m_h5_tk=86d64a702eea3035e5d5a6024012bd40_1551170172203; _m_h5_tk_enc=c10fd504aded0dc94f111b0e77781314; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ5bI3949Xhg%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEzZ1MVSremcx%2BQ%3D&id2=UNcPuUTqrGd03w%3D%3D&nk2=F5RAQ19thpZO8A%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=tb51552614; _l_g_=Ug%3D%3D; ck1=""; unb=3778730506; lgc=tb51552614; cookie1=UUBZRT7oNe6%2BVDtyYKPVM4xfPcfYgF87KLfWMNP70Sc%3D; login=true; cookie17=UNcPuUTqrGd03w%3D%3D; cookie2=1843a4afaaa91d93ab0ab37c3b769be9; _nk_=tb51552614; uss=""; csg=b1ecc171; skt=503cb41f4134d19c; _tb_token_=e13935353f76e; x5sec=7b22726174656d616e616765723b32223a22393031623565643538663331616465613937336130636238633935313935363043493362302b4d46454e76646c7243692b34364c54426f4d4d7a63334f44637a4d4455774e6a7378227d; l=bBIHrB-nvFBuM0pFBOCNVQhjb_QOSIRYjuSJco3Wi_5Bp1T1Zv7OlzBs4e96Vj5R_xYB4KzBhYe9-etui; isg=BDY2WCV-dvURoAZdBw3uwj0Oh2yUQwE5YzQQ9qAfIpm149Z9COfKoZwV-_8q0HKp',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'}
            data = {
                'itemId': item_id,
                'sellerId': 397341302,
                'order': 3,
                'currentPage': page,
                'pageSize': 10,
                'callback': '_DLP_2586_der_3_currentPage_{}_pageSize_10_'.format(page)}
            time.sleep(random.uniform(0.2, 0.3))
            res = requests.get(
                url=url,
                headers=headers,
                params=json.dumps(data))
            res_json = json.loads(res.text[res.text.find('{'):-1])
            rateDetail = res_json.get('rateDetail').get('rateList')
            for one in rateDetail:
                auctionSku = one.get('auctionSku')
                rateContent = one.get('rateContent')
                displayUserNick = one.get('displayUserNick')
                rateDate = one.get('rateDate')
                pics = one.get('pics')
                content = new_one_row + [auctionSku, rateContent, rateDate, displayUserNick, pics]
                with open(r'{}\semir_comment.csv'.format(self.base_dir), mode='a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(content)
            with open(r'{}\alreadydownload.csv'.format(self.base_dir), mode='a', encoding='gbk', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([item_id])
            print('标题:{} ID：{} 总页数：{} 当前页数:{} 保存完成'.format(one_row[2], item_id, one_row[-2], page))

        else:
            pass

    def main(self):
        # for one_row in csv.reader(open(self.path, 'r', encoding='utf-8')):  # 获取每个宝贝评论总页数
        #     self.get_itemid_pages(one_row)
        print('所有的宝贝评论总页数下载完毕\n')
        df = pd.read_csv(r'{}\semir_pages.csv'.format(self.base_dir), encoding='gbk', index_col=False, header=None)
        df[4] = df[4].map(lambda x: str(int(x)))
        df[6] = df[6].map(lambda x: str(int(x)))
        if os.path.exists(r'{}\semir_comment.csv'.format(self.base_dir)):
            with open(r'{}\semir_comment.csv'.format(self.base_dir), mode='r', encoding='utf-8', errors='ignore') as f:
                aa = []
                for one_row in f.readlines():
                    aa.append(one_row[:120].split(','))
            already_df = pd.DataFrame(aa)
            aa_df = already_df[[4, 6]].drop_duplicates()
            aa_df['num'] = '1'
            df2 = df.merge(aa_df, how='left', on=[4, 6])
            df2 = df2.loc[df2['num'] != '1']
            df2.drop(['num'],axis=1, inplace=True)
        else:
            df2 = df

        for one_row in df2.values:
            one_row = one_row.tolist()
            self.get_itemid_comment(one_row)


if __name__ == '__main__':
    path = r'D:\Python\TmallCrawler\UNIQLO_MALE1909.csv'
    tm = tmall_pinglun(path)
    tm.main()
