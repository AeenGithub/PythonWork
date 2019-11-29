# coding: utf-8
import os

# import pandas as pd
import pandas as pd

shop_name = 'ME&CITY'
# os.listdir(r'E:\宝贝详情')
l = os.listdir(r'E:\宝贝详情')
shop_one = [i for i in l if 'Aself' in i]
# shop_one
# l_df = [pd.read_csv(i) for i in shop_one]
# shop_one
shop_one = ['E:\\宝贝详情\\' + i for i in l if shop_name in i]
# shop_one
# l_df = [pd.read_csv(i) for i in shop_one]
# pd.read_csv(shop_one[0])
# pd.read_csv(shop_one[0], encoding='gbk')
# pd.read_csv(shop_one[0], encoding='utf-8')
# shop_one[0]
# os.path.exists(shop_one[0])
# pd.read_csv(shop_one[0])
# pd.read_csv(shop_one[0], engine=Python)
# pd.read_csv(shop_one[0], engine='python')
l_df = [pd.read_csv(i, engine='python') for i in shop_one]
# l_df
Aself = pd.concat(l_df, axis=0, sort=False)
Aself.to_excel('f:{}.xls'.format(shop_name))
print(Aself.shape)