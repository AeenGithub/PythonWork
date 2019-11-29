# coding: utf-8
import pathlib
p = pathlib.Path(r'I:\图片')
all_pic = [i for i in p.iterdir]
all_pic = [i for i in p.iterdir()]
all_pic[0]
all_pic[100]
all_pic[0]
s = all_pic[0]
s.name
for i in all_pic:
    if i.name[0] == '=':
        print(i.name)
        a = i.name
        i.rename(a[1:])
        
print('PyDev console: using IPython .4.0\n')

import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['D:/Python/Python'])
for i in all_pic:
    if i.name[0] == '=':
        print(i.name)
        a = i.name
        new_name = 'I:\\图片\\{}.jpg'.format(a[1:])
        i.rename(new_name)
        
        
import pandas as pd
pd.DataFrame(all_pic)
df = pd.DataFrame(all_pic)
df[0]
df[0][0]
df[0][0].name
df.to_excel(r'I:ok.xls')
get_ipython().run_line_magic('save', 'i:ok.py 1-20')
p = pathlib.Path(r'I:\图片')
all_pic = [i for i in p.iterdir()]
df = pd.DataFrame(all_pic)
df.to_excel(r'I:ok.xls')
df.to_excel(r'I:ok.xls')
get_ipython().run_line_magic('save', 'i:_2.py 1-26')
