# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:33:09 2018

@author: leshuangjiang
"""


import numpy as np
import pandas as pd
import xlwings as xw


def get_excel_data():
    '''打开excel并读取数据'''
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    xb = app.books.open(r"D:\文档\表格\绩效计算\供应商仓检报告HANA(2017.1.1-2017.12.31).xlsx")
    sheet = xb.sheets[0]
    sheet.activate()
    asheet = sheet.range('a1:z100000').options(pd.DataFrame, index=False).value
    xb.close()
    app.quit()
    xw.App.kill(app)
    return asheet

PURCHASE_DIC = {'101': '牛仔',
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
                'A08': 'GSON',
                'A07': '广州产品部',
                'A06': '原点采购组',
                'A10': '潮流运动',
                'A11': '新男装',
                '127': '新商品',
                '105': '配件'}
TATTING_DIC = {'00': '针织', '01': '针织',
               '02': '针织', '03': '外套',
               '04': '衬衫', '05': '衬衫',
               '06': '毛衫', '07': '毛衫',
               '08': '外套', '09': '外套',
               '10': '西服风衣呢', '11': '西服风衣呢',
               '12': '外套', '13': '外套',
               '14': '裙子', '15': '外套',
               '16': '针织', '17': '外套',
               '18': '西服风衣呢', '19': '衬衫',
               '20': '裙子', '21': '裤子',
               '22': '牛仔', '23': '牛仔',
               '24': '牛仔', '25': '裤子',
               '26': '裤子', '27': '裤子',
               '40': '鞋品', '41': '鞋品',
               '42': '鞋品', '43': '鞋品',
               '44': '鞋品', '45': '鞋品',
               '47': '鞋品', '48': '鞋品',
               '50': '泳装', '51': '腰带',
               '52': '袜子', '53': '包',
               '54': '三件套', '55': '帽子',
               '56': '手套', '57': '围巾',
               '58': '领带', '59': '促销品',
               '60': '雨具', '61': '饰品',
               '62': '手表', '70': '套装睡衣',
               '71': '内衣', '72': '长款内裤',
               '73': '短款内裤', '74': '文胸',
               '75': '鞋品', '76': '毛巾',
               '77': '家纺', '90': '公司赠送',
               '91': '物流工服', '92': '品牌推广赠送',
               '93': '外部团体采购', '46': '鞋品'}

def deal_data(rng_sheet):
    '''数据筛选，删除空值'''
    df = rng_sheet.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    df = df.drop(['供应商简称'], axis=1)
    df = df.loc[(df['采购组'] != None) & (df['采购组'].notnull())]
    df['实际采购组'] = df['采购组'].map(PURCHASE_DIC)
    df['款号中类'] = df['款号'].apply(lambda x: TATTING_DIC[x[5:7]])
    df['生产阶段'] = np.where(df['订单属性'].isin(['3']), '测试单', '非测试单')
    df = df.loc[df['款号中类'] != '公司赠送'].copy()
    print('初始数据筛选已经完成')
    return df

def add_tat(df):
    '''将梭织数据和其他数据合并，主要是针对梭织数据要细分同时要保存本身'''
    df_tat = df.loc[df['实际采购组'] == '梭织'].copy()
    df_tat['结果中类'] = df_tat['款号中类']
    df_not_tat = df.loc[df['实际采购组'] != '梭织'].copy()
    df_not_tat['结果中类'] = df_not_tat['实际采购组']
    df_tat_tat = df_tat.copy()
    df_tat_tat['结果中类'] = df_tat_tat['实际采购组']
    result = pd.concat([df_tat, df_not_tat, df_tat_tat], axis=0)
    result['月份'] = result['抽检日期'].str[2:4] + 'M' + result['抽检日期'].str[4:6]
    result['模式'] = result['采购模式'].replace({'Z100': 'CFOB', 'Z101': 'FOB', 'Z102': 'ODM'})
    print('模式和月份已经成功做完')
    return result

def analysis_get_data(result):
    '''生成数据透视表，将数据进行最终结果的制作'''
    c_result = result.pivot_table(index=['正确简称', '结果中类', '模式', '生产阶段', '月份'],
                           columns=['检验结果'], values=['仓检报告编号'],
                           aggfunc=(np.count_nonzero), fill_value=0)
    c_result['次数合计'] = c_result['仓检报告编号']['合格'] + c_result['仓检报告编号']['不合格']
    d_result = result.pivot_table(index=['正确简称', '结果中类', '模式', '生产阶段', '月份'],
                           columns=['检验结果'], values=['出货数量'],
                           fill_value=0, aggfunc=np.sum)
    d_result['数量合计'] = d_result['出货数量']['不合格']+d_result['出货数量']['合格']
    last = pd.merge(d_result, c_result, how='outer', left_index=True, right_index=True)
    lll = last.reset_index()
    lll.to_excel('d:\\仓检结果表.xlsx')
    print('结果保存在--d:\\仓检结果表.xlsx')
    return lll

if __name__ == '__main__':
    try:
        RNG = get_excel_data()
        DFF = deal_data(RNG)
        ADDTAT = add_tat(DFF)
        analysis_get_data(ADDTAT)
    except ValueError as e:
        print(e)
        print('运行失败')

