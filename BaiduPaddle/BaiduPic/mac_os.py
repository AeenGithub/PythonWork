#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

import os
with open(r'config.csv') as f:
    file = f.read()
    all_lines = [i.split(',') for i in file.split('\n')]
print('将要进行名称转换如下：')
for old_name, new_name in all_lines:
    print('''\t{} -------> {}'''.format(old_name, new_name))
judge = input('是否进行转换：（转换请输入：yes）')
if 'yes' == judge:
    for old_name, new_name in all_lines:
        try:
            os.renames(old_name, new_name)
            print('''{} -------> {} 转换成功'''.format(old_name, new_name))
        except:
            print('''{} -------> {} 转换失败'''.format(old_name, new_name))



