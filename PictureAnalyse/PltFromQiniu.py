# -*-coding:utf-8-*-
__author__ = 'AeenPython'

"""
通过将本地图片放在七牛云上，生成外链，然后将外链直接利用拍立淘接口，解析该消费者的上衣穿着
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 13:40:28 2018

@author: leshuangjiang
"""

import copy
import json
import pickle
import random
import re
import time
from datetime import datetime

import requests
from qiniu import Auth, BucketManager, put_file
from qiniu import PersistentFop, urlsafe_base64_encode
from requests_toolbelt import MultipartEncoder


class DealQiNiu(object):
    def __init__(self):
        self.host = 'http://pr7q5c5ea.bkt.clouddn.com'
        self.bucket_domain = self.host[7:]
        access_key = 'Amsb0VBTxOJBlCAhcSmRxA4O8gPLde6MBHoC_UdM'
        secret_key = 'Jl-F0fqFTSzzHWLRa4rTkxnuQw4mZNAPWXtSZ5Pz'
        # 初始化Auth状态
        self.q = Auth(access_key, secret_key)
        # 初始化BucketManager
        self.bucket = BucketManager(self.q)
        # 你要测试的空间， 并且这个key在你空间中存在
        self.bucket_name = 'videopic'

    def get_file_list(self):
        one_pic_lst = []
        # 前缀
        prefix = None
        # 列举条目
        limit = 2549
        delimiter = None
        # 标记
        marker = None
        ret, eof, info = self.bucket.list(self.bucket_name, prefix, marker, limit, delimiter)
        for one_pic in ret['items']:
            one_pic_lst.append(self.host + '/' + one_pic['key'])
        return one_pic_lst

    def picture_thu(self, file_name):
        # 要进行转码的转码操作。
        fops = 'imageMogr2/auto-orient/thumbnail/600x600>/blur/1x0/quality/75|imageslim'
        #  可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
        saveas_key = urlsafe_base64_encode('{}:{}'.format(self.bucket_name, file_name))
        fops = fops + '|saveas/' + saveas_key
        pfop = PersistentFop(self.q, self.bucket_name)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(file_name, ops, 1)
        print(ret)

    def del_file(self, file_name):
        ret, info = self.bucket.delete(self.bucket_name, file_name)
        return info

    def upload_file(self, filepath):
        # filepath is Path
        for one_pic in filepath.iterdir():
            key = one_pic.name
            token = self.q.upload_token(self.bucket_name, key, 3600)
            localfile = one_pic.as_posix()
            ret, info = put_file(token, key, localfile)
            print(info)
        return '--{}--上传完毕'.format(filepath.as_posix())

    def main(self):
        for one_file in self.get_file_list():
            print(one_file)
            #            self.del_file(one_file)
            self.do_private_url(one_file)
        return 'all is finished'


class PaiLiTao(object):
    def __init__(self):
        self.utl_gif = 'http://qhm2.cnzz.com/heatmap.gif'
        self.detail_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'
        self.img_url = 'https://s.taobao.com/image'
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
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            # 'Host': 'www.pailitao.com',
            'Referer': 'http://www.pailitao.com/',
            'Connection': 'keep-alive'
        }
        self.init_cookies = pickle.loads(open(r'D:\Python\PictureAnalyse\taobao_cookies.pickle', 'rb').read())

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

    def search_picture_url(self, picture_url):
        with requests.Session() as s:
            response = s.get(picture_url, headers=self.headers, cookies=self.init_cookies, allow_redirects=False)
            print(response.headers)

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
            response = s.post(self.img_url, headers=post_headers, data=dic)
            # 自动定向到淘宝登陆
            if response.status_code == 200:
                print(response.text)
                tfsid = json.loads(response.text)['name']
                search_payload['tfsid'] = tfsid
                return search_payload
            else:
                print('请求错误')

    def final_get(self, file_name):
        # 获取近似款的宝贝编号
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

    def get_requests(self, itemid):
        # 获取一个itemid的详情信息
        contents = {}
        header = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(itemid)
        }
        date_num = int(
            (datetime.now() - datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds() * 1000)
        get_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=6298b3c5128b9220debf6963eb1d7873&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%22itemNumId%22%3A%22{1}%22'.format(
            date_num, itemid)
        with requests.Session() as s:
            s.get(header['Referer'], headers=header)
            res = s.get(get_url, headers=header, timeout=30)
            time.sleep(random.random() * 5)
            if res.status_code == 200:
                json_data = json.loads(res.text[11:-1])
                # 获取基本信息，商品详细介绍
                if json_data['data'].get('props'):
                    first_key = [i for i in json_data['data'].get('props').keys()][0]
                    for one_dict in json_data['data'].get('props')[first_key]:
                        for one_keys in one_dict.keys():
                            basic_info = one_dict[one_keys]
                            for last_dict in basic_info:
                                for x, y in last_dict.items():
                                    contents[x] = y
                                    return contents
                else:
                    return contents

    def main(self):
        one = r"D:\文档\森马semir\数字化项目组\消费者图库\20190614调研\result\0614_0.jpg"
        item_name = one.split('\\')[-1]
        print(item_name)
        try:
            one_item_lst = self.final_get(one)
            print(one_item_lst)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    pailitao = PaiLiTao()
    filename = r"D:\文档\森马semir\数字化项目组\消费者图库\20190614调研\result\0614_0.jpg"
    # dic = pailitao.upload_file(filename)
    # pylod = pailitao.plt_get(dic)
    # page = pailitao.final_get(filename)
    # print(page)
    # print(pailitao.tfsid_plt_get(filename))
    # picture_url = r'http://www.pailitao.com/search?q=http%3A%2F%2Fpr7q5c5ea.bkt.clouddn.com%2FIMG_20190412_192321-objectsperson-2.jpg&imgfile='
    print(pailitao.main())
    # pailitao.search_picture_url(picture_url)
    # print(pylod)

#
# if __name__ == '__main__':
#     qiniuyun = DealQiNiu()
#     filepath = Path(r'E:\测试e')
#     print(qiniuyun.upload_file(filepath))
#     print(qiniuyun.get_file_list())
