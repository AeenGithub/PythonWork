# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 14:00:23 2018

@author: leshuangjiang
"""
import os
from hashlib import md5


class NameSecret(object):
    def __init__(self):
        self.base_dir = r'E:\森马图库\17weiyi'
        self.pfile = [i[:-4] for i in os.listdir(self.base_dir)]
        self.salt = 'salt6'.encode()
        # 随机生成4位salt

    def rename_stylenum(self):
        for one_style in self.pfile:
            print(one_style)
            one_ss = one_style.encode()
            res = one_ss + self.salt
            md5_obj = md5()
            md5_obj.update(res)
            md = md5_obj.hexdigest()
            old_name = self.base_dir + '\\' + one_style + '.jpg'
            new_name = self.base_dir + '\\' + md + '.jpg'
            os.rename(old_name, new_name)
        return 'all is finished'


if __name__ == '__main__':
    names = NameSecret()
    names.rename_stylenum()
