# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:11:04 2018

@author: leshuangjiang
"""

import pandas as pd
import xlwings as xw


def get_data_fromexcel():
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    xb = app.books.open(r"D:\文档\表格\绩效计算\成本数据1-12.xlsx")
    sheet = xb.sheets[0]
    sheet.activate()
    rng = sheet.range('a1:au100000').options(pd.DataFrame, index=False).value
    xb.close()
    app.quit()
    xw.App.kill(app)
    print('数据已经写入到内存中……\n')
    return rng

def data_screen(rng):
    df = rng.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    df = df.loc[df['中类'] != '公司赠送'].copy()
    df['创建日期'] = df['创建日期'].astype('str')
    df['月份'] = df['创建日期'].str.split('-').str[0].str[-2:] + 'M' + df['创建日期'].str.split('-').str[1]
    df['结果中类'] = df['绩效部门'].copy()
    df_tat = df.loc[(df['绩效部门'] == '外套') | (df['绩效部门'] == '衬衫')
                     |(df['绩效部门'] == '裤子') | (df['绩效部门'] == '裙子')
                     |(df['绩效部门'] == '西服风衣呢')].copy()
    df_tat['结果中类'] = '梭织'
    result = pd.concat([df, df_tat], join='outer', ignore_index=True)
    print('梭织数据已经加入\n')
    return result

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

tatting_dic = {'00': '针织', '01': '针织', '02': '针织', '03': '外套', '04': '衬衫', '05': '衬衫', '06': '毛衫',
               '07': '毛衫', '08': '外套', '09': '外套', '10': '西服风衣呢',  '11': '西服风衣呢',    '12': '外套',
               '13': '外套', '14': '裙子', '15': '外套', '16': '针织', '17': '外套', '18': '西服风衣呢', '19': '衬衫',
               '20': '裙子', '21': '裤子', '22': '牛仔', '23': '牛仔', '24': '牛仔', '25': '裤子',  '26': '裤子',
               '27': '裤子', '40': '鞋品','41': '鞋品', '42': '鞋品', '43': '鞋品', '44': '鞋品', '45': '鞋品',
               '47': '鞋品', '48': '鞋品', '50': '配件', '51': '配件', '52': '配件', '53': '配件', '54': '配件',
               '55': '配件', '56': '配件', '57': '配件', '58': '配件', '59': '促销品', '60': '配件', '61': '配件',
               '62': '配件', '70': '配件', '71': '配件', '72': '配件', '73': '配件', '74': '配件',
               '75': '鞋品', '76': '配件', '77': '配件', '90': '公司赠送', '91': '物流工服',
               '92': '品牌推广赠送', '93': '外部团体采购', '46': '鞋品', '82': '配件', '84': '配件'}
other = {'Y': '原点采购组',
         'G': 'GSON',
         'F': '潮流运动'}


def data_change(result):
    result['加减价金额'] = pd.to_numeric(result['加减价金额'])
    result['标准核价总额'] = pd.to_numeric(result['标准核价总额'])
    result.rename(columns={'订单类型（采购）': '模式', '供应商简称': '正确简称', '采购凭证号': '采购订单号', '物料号': '款号'}, inplace=True)
    group_one = result.groupby(['月份', '正确简称', '结果中类', '模式', '款号'], sort=True)
    second = group_one[ '标准核价总额', '加减价金额'].sum().reset_index()
    ssd = second.groupby([ '月份', '正确简称', '结果中类'])['标准核价总额', '加减价金额'].sum().reset_index()
    ssd.to_excel('d:\\成本偏差结果表.xlsx')
    return '数据已经保存在-d:\\成本偏差结果表.xlsx'


if __name__ == '__main__':
    RNG = get_data_fromexcel()
    SCREEN = data_screen(RNG)
    print(data_change(SCREEN))
    print('all is ok')

