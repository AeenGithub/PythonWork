
# coding: utf-8

# ### 对每家店铺的基本信息数据进行处理

# In[328]:

import os

import numpy as np
import pandas as pd

base_dir = r'D:\Python\TmallCrawler\file\sports'
lst_0827 = [i for i in os.listdir(base_dir) if i.endswith('_1012.xlsx')]
lst_0827 = [base_dir + "\\" + i for i in lst_0827]
one_lst = []
for one in lst_0827:
    print(one)
    Aself = pd.read_excel(one)
    Aself.replace(np.nan, '', inplace=True)
    # 处理上市时间
    detail_time = [i for i in Aself.columns if i.find('上市') >= 0 or i.find('年份') >= 0 or i.find('季节') >= 0]
    Aself['上市安排'] = ''
    Aself['上市安排'] = Aself[detail_time].sum(axis=1)
    Aself['上市安排'] = (Aself['上市安排'].apply(lambda x: [i for i in str(x).split(' ') if len(i) > 6])
                                         .apply(lambda x: ' '.join(x)))
    # 选择列名中出现细节、元素的列名,合并
    detail = [i for i in Aself.columns if i.find('细节') != -1 or i.find('元素') != -1]
    Aself['款式细节点'] = ''
    Aself['款式细节点'] = Aself[detail].sum(axis=1)
    Aself['款式细节点'] = (Aself['款式细节点'].apply(lambda x: set([i for i in str(x).split(' ')]))
                                             .apply(lambda x: ''.join(x)))

    color = [i for i in Aself.columns if i.find('颜色') != -1]
    Aself['分类颜色'] = ''
    Aself['分类颜色'] = Aself[color].sum(axis=1)
    Aself['分类颜色'] = (Aself['分类颜色'].apply(lambda x: set([i for i in str(x).split(' ')]))
                                         .apply(lambda x: ' '.join(x)))

    picture = [i for i in Aself.columns if i.find('图案') != -1]
    Aself['图案点'] = ''
    Aself['图案点'] = Aself[picture].sum(axis=1)
    Aself['图案点'] = (Aself['图案点'].apply(lambda x: set([i for i in str(x).split(' ')]))
                                      .apply(lambda x: ' '.join(x)))

    caizhi = [i for i in Aself.columns if i.find('材质') != -1]
    Aself['材质结果'] = ''
    Aself['材质结果'] = Aself[picture].sum(axis=1)
    Aself['材质结果'] = (Aself['材质结果'].apply(lambda x: set([i for i in str(x).split(' ')]))
                                      .apply(lambda x: ' '.join(x)))

    style_num = [i for i in Aself.columns if i.find('号') != -1]
    Aself['宝贝货号'] = ''
    Aself['宝贝货号'] = Aself[style_num].sum(axis=1)

    Aself['宝贝货号'] = (Aself['宝贝货号'].apply(lambda x: set([i for i in str(x).split(' ')]))
                                         .apply(lambda x: '-'.join(x)))

    # one_Aself = Aself[['item_id', '上市安排', '图案点', '分类颜色', '材质结果', '款式细节点', '宝贝货号']]
    one_Aself = Aself
    one_Aself.replace('', np.nan, inplace=True)
    one_Aself = one_Aself.drop_duplicates()
    one_lst.append(one_Aself)
all_lst = pd.concat(one_lst, ignore_index=True, sort=True)
all_lst.to_excel('d:\\huizong_shop_sports2.xlsx')
