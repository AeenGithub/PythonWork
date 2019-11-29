'''
author: Aeen
'''

import logging
import random
import time
from urllib import request


class Picture(object):

    def __init__(self):
        self.pathfile = r"D:\文档\情报通\brand_stylenum_2"
        # self.headers = {
        #     'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding':'gzip, deflate',
        #     'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        #     'Cache-Control':'max-age=0',
        #     'Connection':'keep-alive',
        #     'Host':'img.alicdn.com',
        #     'If-Modified-Since':'Thu, 09 Aug 2018 13:32:44 GMT',
        #     'Upgrade-Insecure-Requests': '1'}
        self.headers = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
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
        '''just get url from csv'''
        with open(self.pathfile, 'r', newline='', encoding='utf-8') as f:
            for one in f.readlines():
                # print(one.split('	')[1])
                # print(one)
                yield (one.split('	')[0], one.split('	')[1].strip('\t\n'))

    def get_picture(self, img_url, item_id):
        '''get one picture from one url and rename it'''
        print('宝贝', item_id, '开始下载')
        imgurl = '{}'.format(img_url)
        # print(imgurl)
        filename = 'C:\\Users\\leshuangjiang\\Pictures\\天猫图库\情报通\\{}.jpg'.format(item_id)
        # http_handler = request.HTTPHandler()
        # opener = request.build_opener(http_handler)
        try:
            # prequest = request.Request(img_url, self.headers)
            # picture_res = opener.open(prequest)
            # print(picture_res.read().decode('utf-8'))
            # picture_res = requests.get(imgurl, headers=self.headers).content
            request.urlretrieve(imgurl, filename=filename)
            # print(picture_res)
            # with open(filename, 'wb') as fp:
                # fp.write(picture_res)
            print('宝贝', item_id, '下载完成\n')
            time.sleep(random.random())
        except IndexError as e:
            print(e)
        # return item_id, 'completed'

    def main(self):
        for i in self.get_url():
            try:
                item_id, img_url = i
                self.get_picture(img_url, item_id)
            except Exception as e:
                logging.info('{},{}出现问题，需要再次下载'.format(item_id, img_url))
                print(e)
            continue


if __name__ == '__main__':
    p = Picture()
    print(p.main())
    # print(p.get_url().__next__())
