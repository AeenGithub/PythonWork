# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 13:40:28 2018

@author: leshuangjiang
"""

import requests
from qiniu import Auth, BucketManager
from qiniu import PersistentFop, urlsafe_base64_encode


class DealQiNiu():
    def __init__(self):
        host = 'http://pez2d8qzl.bkt.clouddn.com'
        self.bucket_domain = host[7:]
        access_key = 'Amsb0VBTxOJBlCAhcSmRxA4O8gPLde6MBHoC_UdM'
        secret_key = 'Jl-F0fqFTSzzHWLRa4rTkxnuQw4mZNAPWXtSZ5Pz'
        #初始化Auth状态
        self.q = Auth(access_key, secret_key)
        #初始化BucketManager
        self.bucket = BucketManager(q)
        #你要测试的空间， 并且这个key在你空间中存在
        self.bucket_name = 'lachapple'

    def get_file_list(self):
        # 前缀
        prefix = None
        # 列举条目
#        limit = 2549
        delimiter = None
        # 标记
        marker = None
        ret, eof, info = self.bucket.list(self.bucket_name, prefix, marker, delimiter)
        for one in ret['items']:
            key = one['key']
            yield key

    def picture_thu(self, file_name):
        # 要进行转码的转码操作。
        fops = 'imageMogr2/auto-orient/thumbnail/600x600>/blur/1x0/quality/75|imageslim'
        #  可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
        saveas_key = urlsafe_base64_encode('{}:{}'.format(self.bucket_name, file_name))
        fops = fops+'|saveas/'+saveas_key
        pfop = PersistentFop(self.q, self.bucket_name)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(file_name, ops, 1)
        print(ret)

    def do_private_url(self, file_name):
        """设置私人连接"""
        base_url = 'http://%s/%s' % (self.bucket_domain, file_name)
        # 可以设置token过期时间
        private_url = self.q.private_download_url(base_url, expires=3600)
        # print(private_url)
        r = requests.get(private_url)
        print(r)
        pass

    def del_file(self, file_name):
        ret, info = self.bucket.delete(self.bucket_name, file_name)
        return info

    def main(self):
        for one_file in self.get_file_list():
            print(one_file)
            self.del_file(one_file)


if __name__ == '__main__':
    qiniuyun = DealQiNiu()
    qiniuyun.main()
