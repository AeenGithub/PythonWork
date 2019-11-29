'''
author: Aeen
'''

import argparse
import os
import random
import time
from urllib import request

import requests


class Picture(object):
    def __init__(self, dir_name, pathfile):
        dir_name =  dir_name
        # r"D:\文档\商品企划部\A图片下载中心\男衬衫.csv"
        self.pathfile = pathfile
        self.headers = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        base_dir = os.path.split(os.getcwd())[0]
        self.file_dir = os.path.join(base_dir, dir_name)
        if not os.path.exists(self.file_dir ):
            os.makedirs(self.file_dir)

    def get_url(self):
        '''just get url from csv'''
        with open(self.pathfile, 'r', newline='', encoding='utf-8') as f:
            for one in f.readlines():
                # print(one.split('	')[1])
                # print(one)
                yield (one.split(',')[0], one.split(',')[1].strip('\t\n\r'))

    def get_picture(self, img_url, item_id):
        '''get one picture from one url and rename it'''
        print('宝贝', item_id, '开始下载')
        imgurl = '{}'.format(img_url)
        filename = '{}\\{}.jpg'.format(self.file_dir, item_id)
        try:
            if os.path.exists(filename):
                print('宝贝 {} 已经下载完成'.format(item_id))
            else:
                first_image = requests.get(imgurl, timeout=30, headers=self.headers)
                if first_image.status_code == 200:
                    request.urlretrieve(imgurl,filename=filename)
                    print('宝贝', item_id, '下载完成\n')
                    time.sleep(random.random() + 1)
                else:
                    pass
        except IndexError as e:
            print(e)

    def main(self):
        for i in self.get_url():
            try:
                item_id, img_url = i
                # print(img_url)
                self.get_picture(img_url, item_id)
            except Exception as e:
                print(e)
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='输入文件夹名称和链接文件路径')
    parser.add_argument('name', help='输入文件夹名称', default='图片')
    parser.add_argument('file_path', help='图片名称和链接所在文件夹')
    args = parser.parse_args()
    dir_name = args.name
    print('{}文件夹创建成功'.format(dir_name))
    pathfile = args.file_path
    p = Picture(dir_name, pathfile)
    print(p.main())