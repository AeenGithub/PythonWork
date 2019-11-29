# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 16:26:29 2018

@author: leshuangjiang
"""

#import time
#import re
#import os
#import numpy as np
# import numpy as np
import pandas as pd
# import time
# import re
# import os
import xlwings as xw


def get_data_fromexcel():
    app = xw.App(visible=False, add_book=False)
    app.screen_updating = True
    app.display_alerts = False
    xb = app.books.open(r"D:\文档\表格\绩效计算\销售报表 HANA 按月(2017.1-2017.12)(1).xlsx")
    sheet = xw.sheets[0]
    sheet.activate()
    rng = sheet.range('a1:ag100000').options(pd.DataFrame, index=False).value
    print('数据已成功读取到内存\n')
    xb.close()
    app.quit()
    xw.main.App.kill(app)
    return rng

def data_choose(rng):
    df = rng.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    df = df.drop(['供应商简称'], axis=1)
    df = df.loc[df['中类'] != '公司赠送'].copy()
    df = df.loc[(df['采购组'] != None) & (df['采购组'].notnull())
                & (df['零售天数'] != '零售天数') & (df['入库量'] != 0)
                & (df['零售市值'] <= df['配发市值'])]
    df['零售天数'] = pd.to_numeric(df['零售天数'])
    df['入库量'] = pd.to_numeric(df['入库量'])
    df = df.loc[(df['零售量'] > 0)]
    df = df.loc[df['零售天数'] >= 60]
    return df

def add_storage_rate(df):
    style_num = df.groupby(['款号'])['入库量'].sum().reset_index()
    add_storage_rate = pd.merge(df, style_num, how='outer', left_on='款号', right_on='款号')
    add_storage_rate.loc[:,['款号', '入库量_x', '入库量_y']].head()
    df2 =add_storage_rate.loc[add_storage_rate['采购订单号'].str[:2] == '44'].copy()
    return df2


purchase_dic = {'101': '牛仔',
                '102': '针织',
                '104': '毛衫',
                '103': '梭织',
                '106': '鞋品',
                '120': '梭织',
                '121': '梭织',
                '122': '梭织',
                '123': '梭织',
                '124': '针织',
                '125': '毛衫',
                '126': '牛仔',
                'A02': 'GSON',
                'A04': 'GSON',
                'A08': 'GSON',
                'A07': '广州产品部',
                'A06': '原点采购组',
                'A10': '潮流运动',
                'A11': '新男装',
                '127': '新商品',
                '105': '配件'}

tatting_dic = {'00': '针织', '01': '针织', '02': '针织',
               '03': '外套', '04': '衬衫', '05': '衬衫',
               '06': '毛衫', '07': '毛衫', '08': '外套',
               '09': '外套', '10': '西服风衣呢',  '11': '西服风衣呢',
               '12': '外套', '13': '外套', '14': '裙子',
               '15': '外套', '16': '针织', '17': '外套',
               '18': '西服风衣呢', '19': '衬衫', '20': '裙子',
               '21': '裤子', '22': '牛仔', '23': '牛仔',
               '24': '牛仔', '25': '裤子',  '26': '裤子',
               '27': '裤子', '40': '鞋品','41': '鞋品',
               '42': '鞋品', '43': '鞋品', '44': '鞋品',
               '45': '鞋品', '47': '鞋品', '48': '鞋品',
               '50': '配件', '51': '配件', '52': '配件',
               '53': '配件', '54': '配件', '55': '配件',
               '56': '配件', '57': '配件', '58': '配件',
               '59': '促销品', '60': '配件', '61': '配件',
               '62': '配件', '70': '配件', '71': '配件',
               '72': '配件', '73': '配件', '74': '配件',
               '75': '鞋品', '76': '配件', '77': '配件',
               '90': '公司赠送', '91': '物流工服',
               '92': '品牌推广赠送', '93': '外部团体采购',
               '46': '鞋品', '82': '配件', '84': '配件'}

other = {'Y': '原点采购组',
         'G': 'GSON',
         'F': '潮流运动'}
def deal_tat(df2):
    df2['实际采购组1'] = df2['采购组'].map(purchase_dic)
    df2['实际采购组1'].value_counts()
    df2['实际采购组'] = df2['采购组'].map(purchase_dic)
    df2['实际采购组2'] = df2['款号'].str[0].map(other)
    df2.loc[df2['实际采购组2'].notnull(),'实际采购组'] = df2['实际采购组2']
    df2['实际采购组'].value_counts()
    df2['款号中类'] = df2['款号'].apply(lambda x: tatting_dic[x[5:7]])
    df2_tat = df2.loc[df2['实际采购组'] == '梭织'].copy()
    df2_tat['结果中类'] = df2_tat['款号中类']
    s = df2_tat.loc[(df2_tat['款号中类'] == '外套') | (df2_tat['款号中类'] == '裤子')
                       |(df2_tat['款号中类'] == '衬衫') | (df2_tat['款号中类'] == '裙子')
                       |(df2_tat['款号中类'] == '西服风衣呢')].copy()
    df2_tat_tat = s.drop(labels='结果中类', axis=1)
    df2_tat_tat['结果中类'] = df2_tat_tat['实际采购组']
    df2_not_tat = df2.loc[df2['实际采购组'] != '梭织'].copy()
    df2_not_tat['结果中类'] = df2_not_tat['实际采购组']
    result = pd.concat([df2_tat, df2_not_tat, df2_tat_tat], axis=0)
    result['模式'] = result['采购模式'].replace({'Z100': 'CFOB', 'Z101': 'FOB', 'Z102': 'ODM'})
    result['月份'] = result['截止日期'].str[2:4] + 'M'+ result['截止日期'].str[4:6]
    result['实际零售市值'] = result['入库量_x']/result['入库量_y']*result['零售市值']
    result['实际配发市值'] = result['入库量_x']/result['入库量_y']*result['配发市值']
    print('实际零售市值和实际配发市值已经计算完毕……\n')
    return result

def analysis_data(result):
    group_one = result.groupby(['月份', '正确简称', '结果中类', '模式', '款号', '实际零售市值', '实际配发市值'], sort=True)
    second = group_one['采购订单号'].count().reset_index().iloc[:,:7]
    ssd = second.groupby([ '月份', '正确简称', '结果中类', '模式'])['实际零售市值', '实际配发市值'].sum().reset_index()
    ssd.to_excel('d:\\售罄结果表.xlsx')
    print('数据存储在——d:\\售罄结果表.xlsx')
    return ssd

if __name__ == '__main__':
    try:
        get_from_excel = get_data_fromexcel()
        choice = data_choose(get_from_excel)
        add_rate = add_storage_rate(choice)
        deal_tat_data = deal_tat(add_rate)
        analysis_data(deal_tat_data)
    except ValueError as e:
        print(e, '存在问题，请检查')




