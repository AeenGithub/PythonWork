
# coding: utf-8

import pandas as pd
import xlwings as xw

path = r"D:\文档\表格\绩效计算\销售报表 HANA 按月(2017.1-2017.12)(1).xlsx"

def get_data_fromexcel():
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    xb = app.books.open(path)
    sheet = xw.sheets[0]
    sheet.activate()
    rng = sheet.range('a1:ah100000').options(pd.DataFrame, index=False).value
    xb.close()
    app.quit()
    xw.main.App.kill(app)
    return rng

def init_data_deal(rng):
    df = rng.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
# df.fillna(0, inplace=True)
    df = df.drop(['供应商简称'], axis=1)
    df = df.loc[df['中类'] != '公司赠送'].copy()
    df = df.loc[(df['采购组'] != None) & (df['采购组'].notnull())
                & (df['零售天数'] != '零售天数') & (df['入库量'] != 0)]
    df['零售天数'] = pd.to_numeric(df['零售天数'])
    df['入库量'] = pd.to_numeric(df['入库量'])
    df = df.loc[(df['零售量'] > 0)]
    df = df.loc[df['零售天数'] >= 60]
    style_num = df.groupby(['款号'])['入库量'].sum().reset_index()
    style_num.rename(columns={'入库量': '单款总入库量'}, inplace=True)
    add_storage_rate = pd.merge(df, style_num, how='outer', left_on='款号', right_on='款号')
    sty_g_num = df.groupby(['款号', '正确简称'])['入库量'].sum().reset_index()
    sty_g_num.rename(columns={'入库量': '单款单供应商入库量'}, inplace=True)
    df2 = pd.merge(sty_g_num, add_storage_rate, how='outer', left_on=['款号', '正确简称'], right_on=['款号', '正确简称'], suffixes=('_h', '_z'))
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
def get_correct_value(df2):
    df2.loc[:,['款号', '入库量', '单款总入库量',  '单款单供应商入库量']].head(50)
    df2.loc[df2['单款总入库量'] != df2['单款单供应商入库量'], ['款号', '入库量', '单款总入库量',  '单款单供应商入库量']].head()
    df2.loc[df2['款号']=='13037270015', ['款号', '入库量', '单款总入库量',  '单款单供应商入库量']]
    df2.loc[df2['配发市值'] == 0, '配发市值'] = df2.loc[df2['配发市值'] == 0, '零售市值']
    df2['实际采购组1'] = df2['采购组'].map(purchase_dic)
# df['实际采购组'] = df['款号'].str[0].map(other)
    df2['实际采购组1'].value_counts()
    df2['实际采购组'] = df2['采购组'].map(purchase_dic)
    df2['实际采购组2'] = df2['款号'].str[0].map(other)
# df2.loc[df2['款号'].str[0] == '1']
    df2.loc[df2['实际采购组2'].notnull(),'实际采购组'] = df2['实际采购组2']
    df2['实际采购组'].value_counts()
    df2['款号中类'] = df2['款号'].apply(lambda x: tatting_dic[x[5:7]])
    df2['款号中类'].value_counts()
    df2_tat = df2.loc[df2['实际采购组'] == '梭织'].copy()
    df2_tat['结果中类'] = df2_tat['款号中类']
    s = df2_tat.loc[(df2_tat['款号中类'] == '外套') | (df2_tat['款号中类'] == '裤子')
                           |(df2_tat['款号中类'] == '衬衫') | (df2_tat['款号中类'] == '裙子')
                           |(df2_tat['款号中类'] == '西服风衣呢')].copy()
    s['款号中类'].value_counts()
    df2_tat_tat = s.drop(labels='结果中类', axis=1)
    df2_tat_tat['结果中类'] = df2_tat_tat['实际采购组']
    df2_tat_tat['结果中类'].value_counts()
    df2_notTat = df2.loc[df2['实际采购组'] != '梭织'].copy()
    df2_notTat['结果中类'] = df2_notTat['实际采购组']
    result = pd.concat([df2_tat, df2_notTat, df2_tat_tat], axis=0)
    return result

# result.info()
def get_result(result):
    result['模式'] = result['采购模式'].replace({'Z100': 'CFOB', 'Z101': 'FOB', 'Z102': 'ODM'})
    result['月份'] = result['截止日期'].str[2:4] + 'M'+ result['截止日期'].str[4:6]
    result['月份'].head()
    result['截止日期'] = pd.to_datetime(result['截止日期'])
    result['实际零售市值'] = result['单款单供应商入库量']/result['单款总入库量']*result['零售市值']
    result['实际配发市值'] = result['单款单供应商入库量']/result['单款总入库量']*result['配发市值']
    result['最小值'] = result.loc[:,['实际零售市值', '实际配发市值', '入库市值']].min(axis=1)
    result['实际售罄率'] = result['实际零售市值']/result['实际配发市值']
    result['修正配发市值'] = result['实际配发市值']
    result['修正零售市值'] = result['实际零售市值']
    result.loc[result['实际售罄率'] > 1, '修正配发市值'] = result.loc[result['实际售罄率'] > 1]['最小值']
    result.loc[result['实际售罄率'] > 1, '修正零售市值'] = result.loc[result['实际售罄率'] > 1]['最小值']
    result = result.loc[result['采购订单号'].str[:2] == '44'].copy()
    result.loc[(result['款号'] == '13037270015') & (result['月份'] == '17M03') & (result['正确简称'] == '顺得利(好兄妹)'), ['月份', '正确简称', '修正配发市值', '修正零售市值']].round(2)
    group_one = result.groupby(['月份', '正确简称', '结果中类', '模式', '款号', '修正零售市值', '修正配发市值'], sort=True)
    second = group_one['采购订单号'].count().reset_index().iloc[:,:7]
    ssd = second.groupby([ '月份', '正确简称', '结果中类', '模式'])['修正零售市值', '修正配发市值'].sum().reset_index()
    ssd.to_excel('d:\\售罄结果表.xlsx')
    return '数据已经保存在-d:\\售罄结果表.xlsx'

if __name__=='__main__':
    RNG = get_data_fromexcel()
    FIRST = init_data_deal(RNG)
    CORRECT = get_correct_value(FIRST)
    print(get_result(CORRECT))