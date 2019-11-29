'''
author: Aeen
'''

import json
import logging
import pickle
import random
import time
from datetime import datetime
from pathlib import Path
from urllib import request

import pandas as pd
import requests
from lxml import etree


class Picture(object):

    def __init__(self):
        self.pathfile = r"D:\Python\TmallCrawler\file\190504\启初_0504.xlsx"
        self.headers = {
            'Host': "h5api.m.taobao.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
            'Accept': "*/*",
            'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            'Accept-Encoding': "gzip, deflate, br",
            'Referer': "https://h5.m.taobao.com/app/detail/desc.html?_isH5Des=true",
        }
        self.get_log()

    def get_log(self):
        '''通过使用logging包将程序运行出错的地方进行记录'''
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='D:\\爬虫日志\\Tmall_picture_download.log',
                            filemode='w')

    def get_url(self):
        df = pd.read_excel(self.pathfile)
        new_df = df.loc[:, ['itemId', 'taobaoPcDescUrl', 'sell_video', 'images', 'moduleDescParams_f']].copy()
        new_df.set_index('itemId', inplace=True)
        new_df.fillna('', inplace=True)
        new_df = new_df.applymap(lambda x: x.replace('//', 'https://'))
        taobaoPcDescUrl_dict = new_df['taobaoPcDescUrl'].to_dict()
        images_dict = new_df['images'].str.split(',').to_dict()
        new_df['sell_video'] = new_df['sell_video'].str.replace('https:https:', 'https:')
        new_df['sell_video'] = new_df['sell_video'].apply(lambda x: x.split('?')[0])
        sell_video_dict = new_df.loc[new_df['sell_video'] != '', 'sell_video'].to_dict()
        return (taobaoPcDescUrl_dict, images_dict, sell_video_dict)

    def make_every_dir(self, itemid):
        file = Path(self.pathfile)
        new_file_path = file.parent.joinpath('{}'.format(itemid))
        try:
            new_file_path.mkdir(exist_ok=False)  # 当False时不对已经建立的文件夹进行覆盖
        except FileExistsError as e:
            print('文件夹已经存在')
        return new_file_path

    def get_picture_download(self, img_url, item_id, new_file_path):
        '''get one picture from one url and rename it'''
        print('宝贝', item_id, '开始下载')
        imgurl = '{}'.format(img_url)
        filename = '{}\\{}.jpg'.format(new_file_path, item_id)
        if not Path(filename).exists():
            try:
                request.urlretrieve(imgurl, filename=filename)
                print('宝贝', item_id, '下载完成\n')
                time.sleep(random.random())
            except IndexError as e:
                print(e)

    def images_main(self):
        taobaoPcDescUrl_dict, images_dict, sell_video_dict = self.get_url()
        for item_id, img_urls in images_dict.items():
            # 根据item_id创建文件夹
            new_file_path = self.make_every_dir(item_id)
            # 将图片链接提取出来，一一下载
            if isinstance(img_urls, list):
                for index, img_url in enumerate(img_urls):
                    item_id_img = '{}_{}'.format(item_id, index+1)
                    try:
                        self.get_picture_download(img_url, item_id_img, new_file_path)
                    except Exception as e:
                        logging.info('{},{}出现问题，需要再次下载'.format(item_id_img, img_url))
                        print(e)
                    continue

    def video_main(self):
        taobaoPcDescUrl_dict, images_dict, sell_video_dict = self.get_url()
        for item_id, video_url in sell_video_dict.items():
            new_file_path = self.make_every_dir(item_id)
            video_file = new_file_path.joinpath('{}.mp4'.format(item_id))
            if not video_file.exists():
                try:
                    request.urlretrieve(video_url, video_file)
                    print('宝贝', item_id, '下载完成\n')
                    time.sleep(random.random())
                except:
                    logging.info('{},{}出现问题，需要再次下载'.format(item_id, video_url))
                    continue

    def Tmall_detail_picture(self, taobaoPcDescUrl_dict):
        headers = {
            'Host': "h5api.m.taobao.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
            'Accept': "*/*",
            'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            'Accept-Encoding': "gzip, deflate, br",
            'Referer': "https://h5.m.taobao.com/app/detail/desc.html?_isH5Des=true",
        }
        all_files = []
        for item_id, detail_url in list(taobaoPcDescUrl_dict.items()):
            print('{}正在访问'.format(item_id))
            f_code = detail_url.split('&')[2].split('=')[1]
            date_num = int((datetime.now() - datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds() * 1000)
            url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdesc/6.0/?jsv=2.4.11&appKey=12574478&t={}&api=mtop.taobao.detail.getdesc&v=6.0&type=jsonp&dataType=jsonp&timeout=20000&callback=mtopjsonp1&data=%7B%22id%22%3A%22{}%22%2C%22type%22%3A%222%22%2C%22f%22%3A%22{}%22%7D'.format(
                date_num, item_id, f_code)
            response = requests.request("GET", url, headers=headers)
            time.sleep(random.random()*5)
            json_data = json.loads(response.text[11:-1])
            detail_html = etree.HTML(json_data['data']['pcDescContent'])
            one_lst = []
            for i in detail_html.cssselect('img'):
                img_detail_url = i.attrib['src']
                one_lst.append(img_detail_url)
            all_files.append((item_id, one_lst))
        with open('item_one_lst', 'wb') as f:
            f.write(pickle.dumps(all_files))
        return all_files

    def Tmall_detail_download(self, item_one_lst):
        for item_id, one_lst in item_one_lst:
            # 根据item_id建立文件夹
            new_file_path = self.make_every_dir(item_id)
            # 在每个item_id文件夹中建立详情页文件夹
            detail_file_path = new_file_path.joinpath('详情页')
            try:
                new_file_path.joinpath('详情页').mkdir()
            except FileExistsError as e:
                print('\t', e, '文件夹已经存在')
            for index, one_picture_url in enumerate(one_lst):
                suffix = one_picture_url[-3:]
                one_picture_url = 'https:' + one_picture_url
                # 根据链接得文件格式，生成本地文件名,放入新建立的detail_file_path中
                new_file_name = detail_file_path.joinpath('{}_{}.{}'.format(item_id, index+1, suffix))
                if not new_file_name.exists():
                    try:
                        request.urlretrieve(one_picture_url, new_file_name)
                        time.sleep(random.random())
                        print('{}下载完成'.format(new_file_name))
                    except Exception as e:
                        print(e)
                        pass
        return '所有的宝贝详情页都已经下载完毕'

    def Tmall_detail_main(self):
        taobaoPcDescUrl_dict, images_dict, sell_video_dict = self.get_url()
        item_one_lst = self.Tmall_detail_picture(taobaoPcDescUrl_dict)
        with open('item_one_lst', 'rb') as f:
            item_one_lst = pickle.loads(f.read())
        print(self.Tmall_detail_download(item_one_lst))
        return 'ok'

if __name__ == '__main__':
    p = Picture()
    print(p.video_main())
    print(p.images_main())
    print(p.Tmall_detail_main())
    # print(p.get_url().__next__())
