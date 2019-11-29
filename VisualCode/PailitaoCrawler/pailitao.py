# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 14:42:44 2018
@author: leshuangjiang
"""
import copy
import json
import os
import random
import re
from datetime import datetime

import pandas as pd
import requests
from requests_toolbelt import MultipartEncoder


# sys.stdout=io.TextIOWrapper(sys.stdout.,encoding='utf-8')


class PaiLiTao(object):
    def __init__(self):
        self.utl_gif = 'http://qhm2.cnzz.com/heatmap.gif'
        self.detail_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'
        self.img_url = 'http://www.pailitao.com/image'
        self.search_url = 'http://www.pailitao.com/search'
        self.payload = {
            'a': '0',
            'b': 'firefox',
            'c': '1',
            'id': '1255152583',
            'p': 'http://www.pailitao.com/',
            'r': 'https://www.baidu.com/link?url=Zb-5-h4lTqhAlfurcDnefmNYVqogA_AjXHwrCz0MfMEo31EOv_Ek9lmu7DLJkCXU&wd=&eqid=bb94621c000533db000000045b9a04aa',
            'random': 'Thu Sep 13 2018 14:56:38 GMT+0800',
            's': '1600x900',
            'w': '1012',
            'x': '618',
            'y': '425'
        }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.pailitao.com/',
            'Connection': 'keep-alive'
        }

    def upload_file(self, file_name):
        # 上传文件
        upload_file = MultipartEncoder(
            fields={
                'imgfile': ('filename', open(file_name, 'rb'), 'image/jpeg')
            },
            boundary='---------------------------' +
                     str(random.randint(250000000000000, 300000000000000))
        )
        return upload_file

    def tfsid_plt_get(self, file_name):
        # 获取第三次请求参数tfsid
        search_payload = {
            'q': '+',
            'imgfile': '',
            'app': 'imgsearch'
        }
        dic = self.upload_file(file_name)
        with requests.Session() as s:
            s.get(self.utl_gif, params=self.payload, headers=self.headers)
            post_headers = copy.deepcopy(self.headers)
            post_headers['Content-Type'] = dic.content_type
            post_headers['X-Requested-With'] = 'XMLHttpRequest'
            post_headers['Content-Length'] = '641068'
            post_headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            response = requests.post(self.img_url, headers=post_headers, data=dic)
            # 自动定向到淘宝登陆
            if response.status_code == 200:
                print(response.text)
                tfsid = json.loads(response.text)['name']
                search_payload['tfsid'] = tfsid
                return search_payload
            else:
                print('请求错误')

    def final_get(self, file_name):
        # 获取近似款的信息
        one_page_item = []
        pylod = self.tfsid_plt_get(file_name)
        final_headers = copy.deepcopy(self.headers)
        final_headers['Host'] = 'www.pailitao.com'
        final_headers['Accept'] = 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8'
        final_response = requests.get(self.search_url, params=pylod)
        page = final_response.text
        need = re.findall('g_page_config = (.*"map":{}})', page)[0]
        need_json = json.loads(need)
        lst_item = need_json['mods']['itemlist']['data']['collections'][0]
        for one_auction in lst_item['auctions']:
            item_id = one_auction['detail_url'].split('=')[1].replace('&ns', '')
            one_page_item.append(item_id)
        return one_page_item[:10]

    def h5_taobao_url(self, item_id):
        item_id_url = 'https://h5.m.taobao.com/awp/core/detail.htm?id=' + item_id
        datenum = int((datetime.now() - datetime.strptime('1970-01-01 00:00:00',
                                                          '%Y-%m-%d %H:%M:%S')).total_seconds() * 1000)
        one = '{"itemNumId":"'
        two = '","exParams":"{\\"ft\\":\\"t\\",\\"id\\":\\"'
        three = '\\"}","detail_v":"3.1.1","ttid":"2018@taobao_iphone_9.9.9"}'
        data = ''.join([one, item_id, two, item_id, three])
        detail_payloads = {
            'AntiCreep': 'true',
            'AntiFlood': 'true',
            'api': 'mtop.taobao.detail.getdetail',
            'appKey': '12574478',
            'callback': 'mtopjsonp1',
            'dataType': 'jsonp',
            'ecode': '0',
            'H5Request': 'true',
            'isSec': '0',
            'jsv': '2.4.11',
            't': str(datenum),
            'ttid': '2018@taobao_iphone_9.9.9',
            'type': 'jsonp',
            'utdid': '123123123123123',
            'v': '6.0',
            'data': data
        }
        detail_headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Referer': 'https://h5.m.taobao.com/awp/core/detail.htm?ft=t&id={}'.format(item_id)
        }
        with requests.Session() as s:
            s.get(item_id_url, headers=detail_headers)
            detail = s.get(self.detail_url, headers=detail_headers,
                           params=detail_payloads)
        json_data = json.loads(detail.text[11:-1])
        try:
            basic_info_local = json_data['data']['props']['groupProps'][0]['基本信息']
            item_title = json_data['data']['item']['title']
            basic_info_local.append({'title': item_title})
            return basic_info_local
        except:
            pass

    def h5_tao_url_2(self):
        url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'
        datenum = int((datetime.now() - datetime.strptime('1970-01-01 00:00:00',
                                                          '%Y-%m-%d %H:%M:%S')).total_seconds() * 1000)
        one = '{"itemNumId":"'
        two = '","exParams":"{\\"ft\\":\\"t\\",\\"id\\":\\"'
        three = '\\"}","detail_v":"3.1.1","ttid":"2017@taobao_h5_6.6.0"}'
        data = ''.join([one, item_id, two, item_id, three])
        detail_payloads = {
            'AntiCreep': 'true',
            'api': 'mtop.taobao.detail.getdetail',
            'appKey': '12574478',
            'callback': 'mtopjsonp2',
            'dataType': 'jsonp',
            'jsv': '2.4.8',
            't': str(datenum),
            'ttid': '2017@taobao_h5_6.6.0',
            'type': 'jsonp',
            'v': '6.0',
            'data': data
        }
        detail_headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Referer': 'https://h5.m.taobao.com/awp/core/detail.htm?ft=t&id={}'.format(item_id)
        }
        with requests.Session() as s:
            s.get(item_id_url, headers=detail_headers)
            detail = s.get(self.detail_url, headers=detail_headers,
                           params=detail_payloads)
        json_data = json.loads(detail.text[11:-1])
        try:
            basic_info_local = json_data['data']['props']['groupProps'][0]['基本信息']
            item_title = json_data['data']['item']['title']
            basic_info_local.append({'title': item_title})
            return basic_info_local
        except:
            pass

    def get_item_detail(self, file_name):
        page_basic_info = []
        item_id_lst = self.final_get(file_name)
        print(item_id_lst)
        for one_item_id in item_id_lst:
            dic = {}
            print('近似款的ID: ', one_item_id)
            basic_info = self.h5_taobao_url(one_item_id)
            if bool(basic_info) is False:
                basic_info = self.h5_tao_url_2(one_item_id)
            else:
                pass
            if basic_info:
                for one_dic in basic_info:
                    x, y = list(one_dic.items())[0]
                    dic[x] = y
            else:
                pass
            df_basic_info = pd.DataFrame([dic])
            df_basic_info['item_id'] = one_item_id
            page_basic_info.append(df_basic_info)
        df_page_basic_info = pd.concat(
            page_basic_info, ignore_index=True, sort=True)
        return df_page_basic_info

    def main(self):
        all_df = []
        base_dir = 'E:\\街拍拍立淘测试'
        p = [base_dir + "\\" + i for i in os.listdir(base_dir)]
        for one in p:
            print(one)
            item_name = one.split('\\')[-1]
            try:
                one_item_lst = self.final_get(one)
                all_df.append({one, one_item_lst})
            except Exception as e:
                print(e)
                pass
            continue
        all_df_res = pd.DataFrame(all_df)
        all_df_res.to_excel('d:\\test\\jiepai_res3.xlsx')
        print('all is ok')


if __name__ == '__main__':
    pailitao = PaiLiTao()
    # filename = r"E:\街拍拍立淘测试\IMG_3420-objectsperson-6.jpg"
    # dic = pailitao.upload_file(filename)
    # pylod = pailitao.plt_get(dic)
    # page = pailitao.final_get(filename)
    # print(page)
    # print(pailitao.tfsid_plt_get(filename))
    print(pailitao.main())
    # print(pylod)
