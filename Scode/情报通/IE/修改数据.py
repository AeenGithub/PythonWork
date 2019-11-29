#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

import pandas as pd


def write_in_pickle():
    df = pd.read_clipboard()
    df.to_pickle('brand_senior')
    df.to_excel('brand_senior.xlsx')
    print('修改成功！')

write_in_pickle()

