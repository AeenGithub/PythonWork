# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 13:40:28 2018

@author: leshuangjiang
"""

from pathlib import Path

from qiniu import Auth, BucketManager
from qiniu import PersistentFop, urlsafe_base64_encode
from qiniu import put_file


class DealQiNiu():
    def __init__(self):
        self.host = 'http://pr7q5c5ea.bkt.clouddn.com'
        self.bucket_domain = self.host[7:]
        access_key = 'Amsb0VBTxOJBlCAhcSmRxA4O8gPLde6MBHoC_UdM'
        secret_key = 'Jl-F0fqFTSzzHWLRa4rTkxnuQw4mZNAPWXtSZ5Pz'
        #初始化Auth状态
        self.q = Auth(access_key, secret_key)
        #初始化BucketManager
        self.bucket = BucketManager(self.q)
        #你要测试的空间， 并且这个key在你空间中存在
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
        fops = fops+'|saveas/'+saveas_key
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
        

if __name__ == '__main__':
    qiniuyun = DealQiNiu()
    filepath = Path(r'E:\测试e')
    print(qiniuyun.upload_file(filepath))
    print(qiniuyun.get_file_list())

