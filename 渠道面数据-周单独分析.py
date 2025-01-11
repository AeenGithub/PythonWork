# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 19:07:55 2019

@author: leshuangjiang
"""

import pandas as pd 
import numpy as np
import os
from pathlib import Path
from datetime import datetime, timedelta
import xlwings as xw


# pd.set_option('display.min_rows', 300)

week_n = 201951
month_n = 201912
month_b = 201910


date_n =  20191222
quarter_n = [month_b, 201911, 201912]

now_strtime = datetime.strptime(str(date_n), '%Y%m%d')

week_l = week_n - 100
l_month_n = month_n - 100
l_month_b = month_b - 100

base_dir = 'D:\文档\S&OP项目\荣叔报表'
# ## 读取数据
# ### 销售数据转化为8个加盟渠道和5个直营分公司和性格修改表

config_where_df = pd.read_csv(r"D:\文档\S&OP项目\配置文件\加盟直营渠道对照表.csv")
config_gender_df = pd.read_csv(r'D:\文档\S&OP项目\配置文件\性别修改表.csv')


# ### 零售数据2019年

sale_2019_df = pd.read_csv(r"{}\{}\sales2019.csv".format(base_dir, date_n), skiprows=26)
sale_2019_df = sale_2019_df.merge(config_where_df, on=['销售地区名称', '营销区域名称'])

# ### 配发数据指定产品季(18S78和19S78，配发数据匹配大区
allotment_df = pd.read_csv(r"{}\{}\retail2019.csv".format(base_dir, date_n), skiprows=28)
allotment_df = allotment_df.merge(config_where_df, on=['销售地区名称', '营销区域名称'])

# ### 采购到货数据，知道每个款的采购成本
purchase_df = pd.read_csv(r"{}\{}\purchase-至今.csv".format(base_dir, date_n), skiprows=10)
purchase_df['成本价'] = purchase_df['实际入库金额'] / purchase_df['实际入库数量']


# ### 库存数据（仅到大区和产品季）、同店可比分析数据源
# #### 库存筛选直营和加盟17产品年及以后的数据
stock_2019_df = pd.read_csv(r"{}\{}\stock2019.csv".format(base_dir, date_n), skiprows=30)
stock_2019_df = stock_2019_df.merge(config_where_df, on=['销售地区名称', '营销区域名称'])
stock_2019_df = stock_2019_df.loc[~stock_2019_df['产品季'].str.contains('2017Q|2018Q|2019Q|2020Q')]
stock_2019_df = stock_2019_df.loc[stock_2019_df['产品年'] >= 2017]

# ### 同店可比数据
compare_df = pd.read_csv(r"{}\{}\compare-至今.csv".format(base_dir, date_n), skiprows=26)
compare_df = compare_df.merge(config_where_df, on=['销售地区名称', '营销区域名称'])

# ### 周零售数据到天，计算同店同比
week_compare = pd.read_csv(r"{}\{}\week\week_compare.csv".format(base_dir, date_n), skiprows=26)
week_compare = week_compare.merge(config_where_df, on=['销售地区名称', '营销区域名称'])


week_sales = pd.read_csv(r"{}\{}\week\week_sales.csv".format(base_dir, date_n), skiprows=26)
week_sales = week_sales.merge(config_where_df, on=['销售地区名称', '营销区域名称'])



def get_new_product_stock(df, prod_year):
    '''输入产品年，新品库存数量和库存市值'''
    new_product_stock = df.loc[df['产品年'] == prod_year].groupby(['渠道', '大区'])['门店历史库存市值', '门店历史库存'].sum()
    new_product_stock.columns = ['新品门店历史库存市值', '新品门店历史库存']
    return new_product_stock

# 产品年
stock_sum_2019_df = stock_2019_df.groupby(['渠道', '大区'])['门店历史库存', '门店历史库存市值'].sum()
new_stock_2019 = get_new_product_stock(stock_2019_df, 2019)


allotment_df['年份'] = np.where(allotment_df['产品季'].str.contains('2018'), '18冬配发', '19冬配发')
allotment_year = allotment_df.groupby(['年份', '渠道', '大区'])['配发量'].sum().unstack(0)


allotment_2019 = allotment_year['19冬配发']
allotment_2019.name = '配发量'

# ## 计算环节
# 1. 确定好18年和19年本周的时间，然后确定当月时间，再确定本季时间
# 2. 修改了毛利率的计算逻辑，现在使用零售毛利率， （零售额-采购额）/零售额
# 3. 全部产品的动销率，采用本周零售量/（零售量+库存量
# 

# ### 计算周的相关指标

week_data = week_sales.loc[week_sales['年份周(20161)'].isin([201851, 201951])].copy()

week_data_2018 = week_data.drop(columns=['当期零售金额', '当期零售数量', '当期零售市值'])
week_data_2018.rename(columns={'零售金额同期': '当期零售金额',
                         '零售数量同期': '当期零售数量',
                         '零售市值同期': '当期零售市值'}, inplace=True)
week_data_2019 = week_data.copy()

# 本周的计算，18年和19年的零售金额、同店零售金额、零售量、本周S78的累计配发量、本周全部产品的库存量、零售市值、
# 本周起始时间：2019-12-16至2019-12-31，本周是19年52周

def calcul_week_money(df, yweek, stock_sum_df):
    week_df = df[df['年份周(20161)'] == yweek]
    sales_df = week_df.groupby(['渠道', '大区'])['当期零售金额', '当期零售数量', '当期零售市值'].sum()
    sales_df.columns = ['周当期零售金额', '周当期零售数量', '周当期零售市值']
    return sales_df

sales_week_2019 = calcul_week_money(week_data_2019, 201951, stock_sum_2019_df)

# 周--19冬产品季的动销计算

def calcu_season_count(df, yearweek, prod_lst):
    '''指定产品季和时间段的零售数量，计算动销'''
    season_week_df = df[(df['年份周(20161)'] == yearweek) & (df['产品季'].isin(prod_lst))]
    season_sales = pd.DataFrame(season_week_df.groupby(['渠道', '大区'])['当期零售数量', '当期零售金额', '当期零售市值'].sum())
    season_sales.columns = ['周当季零售数量', '周当季零售金额', '周当季零售市值']
    return season_sales


# 周--19冬产品季的毛利率计算
def cal_profit_week(df, yweek):
    '''计算指定时间范围内的成本额和毛利率'''
    week_df = df[df['年份周(20161)'] == yweek]
    week_profit_df = week_df.groupby(['渠道', '大区', '款号'])['当期零售金额', '当期零售数量'].sum().reset_index().merge(purchase_df[['款号', '成本价']], on=['款号'])
    week_profit_df['成本额'] = week_profit_df['当期零售数量'] * week_profit_df['成本价']
    week_profit_res = week_profit_df.groupby(['渠道', '大区'])['当期零售金额', '成本额'].sum()
    week_profit_res.columns = ['周当期零售金额', '周成本额']
    week_profit_res = week_profit_res[['周成本额']]
    return week_profit_res

S78_sales_week_2019 = calcu_season_count(week_data_2019, week_n, ['2019S7', '2019S8'])
profit_week_2019_df = cal_profit_week(week_data_2019, week_n)

# ### 本月的数据，从本月1号到本月当前查询时间

def calcul_month_money(df, ymonth, stock_sum_df):
    week_df = df.loc[(df['年份月份 (201601)'] == ymonth)]
    sales_df = week_df.groupby(['渠道', '大区'])['当期零售金额', '当期零售数量', '当期零售市值'].sum()
    sales_df.columns =  ['月当期零售金额', '月当期零售数量', '月当期零售市值']
    return sales_df

sales_month_2019 = calcul_month_money(sale_2019_df, 201912, stock_sum_2019_df)

# 月--毛利率计算

def cal_profit_month(df, ymonth, yweek):
    week_df = df.loc[(df['年份月份 (201601)'] == ymonth)]
    week_profit_df = week_df.groupby(['渠道', '大区', '款号'])['当期零售金额', '当期零售数量'].sum().reset_index().merge(purchase_df[['款号', '成本价']], on=['款号'])
    week_profit_df['成本额'] = week_profit_df['当期零售数量'] * week_profit_df['成本价']
    week_profit_res = week_profit_df.groupby(['渠道', '大区'])['当期零售金额', '成本额'].sum()
#     week_profit_res['品牌毛利率'] = (week_profit_res['当期零售金额'] - week_profit_res['成本额']) / week_profit_res['当期零售金额']
    week_profit_res = week_profit_res[['成本额']]
    week_profit_res.columns =  ['月成本额']
    return week_profit_res

profit_2019_month_df = cal_profit_month(sale_2019_df, 201912, week_n)

# ### 本季度的数据，指定查询时间的所有数据
# 本季度就是多个月的和

#     sales_df['折扣'] = sales_df['当期零售金额']/sales_df['当期零售市值']
#     total_sale_rate = sales_df.join(stock_sum_df)
#     total_sale_rate['全部产品本周动销率'] = total_sale_rate['当期零售数量'] / (total_sale_rate['当期零售数量'] + total_sale_rate['门店历史库存'])
#     result_df = sales_df.join(total_sale_rate[['门店历史库存', '全部产品本周动销率']])
def calcul_quater_money(df, year, ymonth_lst, stock_sum_df):
    week_df = df.loc[df['年份月份 (201601)'].isin(ymonth_lst)]
    sales_df = week_df.groupby(['渠道', '大区'])['当期零售金额', '当期零售数量', '当期零售市值'].sum()
    sales_df.columns = ['季度当期零售金额', '季度当期零售数量', '季度当期零售市值']
    return sales_df


sales_quarter_2019 = calcul_quater_money(sale_2019_df, 2019, quarter_n, stock_sum_2019_df)

# 季度--19冬产品季的动销计算
def calcu_quarter_count(df, ymonth_lst, prod_lst):
    quarter_week_df = df.loc[(df['年份月份 (201601)'].isin(ymonth_lst)) & (df['产品季'].isin(prod_lst))]
    quarter_sales = pd.DataFrame(quarter_week_df.groupby(['渠道', '大区'])['当期零售数量', '当期零售金额', '当期零售市值'].sum())
    quarter_sales.columns = ['季度当季零售数量', '季度当季零售金额', '季度当季零售市值']
    return quarter_sales

# 季度--毛利率计算
def cal_profit_quarter(df, year, ymonth_lst):
    '''计算季度的毛利率'''
    quarter_df = df.loc[df['年份月份 (201601)'].isin(ymonth_lst)]
    quarter_profit_df = quarter_df.groupby(['渠道', '大区', '款号'])['当期零售金额', '当期零售数量'].sum().reset_index().merge(purchase_df[['款号', '成本价']], on=['款号'])
    quarter_profit_df['成本额'] = quarter_profit_df['当期零售数量'] * quarter_profit_df['成本价']
    quarter_profit_res = quarter_profit_df.groupby(['渠道', '大区'])['成本额'].sum()
#     quarter_profit_res['品牌毛利率'] = (quarter_profit_res['当期零售金额'] - quarter_profit_res['成本额']) / quarter_profit_res['当期零售金额']
    quarter_profit_res.name = '季度成本额'
    return quarter_profit_res.to_frame()


S78_sales_quarter_2019 = calcu_quarter_count(sale_2019_df, quarter_n, ['2019S7', '2019S8'])
profit_2019_quarter_df = cal_profit_quarter(sale_2019_df, 2019, quarter_n)

def sale_weeks(df, yearquarter):
    '本季度截至当前的周数'
    week_df = df.loc[df['年份月份 (201601)'].isin(yearquarter)]
    return pd.DataFrame(week_df.groupby(['渠道', '大区'])['年份周(20161)'].agg(销售周数=lambda x: x.max() - x.min() + 1))
sale_weeks_df = sale_weeks(sale_2019_df, quarter_n)

# ### 近13周的平均零售量和近3个月的平均零售市值，计算可销周数和可销月数
#### 12月1日，起始时间是多少，12月31日，起始月份是多少, 由于数据的问题，没办法取到天，还是三个月，选择13个周，滚动13周
def thirteen_yweeks(year, now_strtime):
    before_thirteen_day = now_strtime - timedelta(weeks=12)
    before_thirteen_week = datetime.isocalendar(before_thirteen_day)[1]
    begin_13_yweek = int('{}{:02d}'.format(year, before_thirteen_week))
    now_yweek = datetime.isocalendar(now_strtime)[1]
    end_13_yweek = int('{}{:02d}'.format(year, now_yweek))
    return begin_13_yweek, end_13_yweek

def avg_sales(df, year, begin_13_yweek_2018, end_13_yweek_2018):
    sale_thirteen = df.loc[(df['年份周(20161)'] >= begin_13_yweek_2018) & (df['年份周(20161)'] <= end_13_yweek_2018)]
    avg_sales = sale_thirteen.groupby(['渠道', '大区'])['当期零售数量', '当期零售市值'].sum()
    avg_sales['库存平均13周当期零售数量'] = avg_sales['当期零售数量']/13
    avg_sales['库存平均3月当期零售市值'] = avg_sales['当期零售市值']/3
    avg_sales.drop(columns=['当期零售数量', '当期零售市值'], inplace=True)
    return avg_sales


begin_13_yweek_2019, end_13_yweek_2019 = thirteen_yweeks(2019, now_strtime)
avg_sales_2019 = avg_sales(sale_2019_df, 2019, begin_13_yweek_2019, end_13_yweek_2019)


# ### 同店同比的零售板块的计算：当期零售金额, 当期零售数量, 当期零售市值，折扣，同店同比单独计算
def compare_rate(times, df):
    '''计算不同时期的门店同店同比对应值'''
    df2 = df.groupby(['渠道', '大区'])['当期零售金额'].sum().to_frame()
    df2['零售金额同期'] = df.groupby(['渠道', '大区'])['零售金额同期'].sum()
    df2.columns = [f'{times}同店当期零售金额', f'{times}同店同期零售金额']
    return df2

# 计算周可比，选取不同年份的同周数据
week_compare.fillna(0,inplace=True)
df2 = week_compare.groupby(['星期几(星期五) ','新主门店识别编码'])['当期零售金额','零售金额同期'].sum().reset_index()
df2['是否可比店'] = np.where((df2['当期零售金额']>0) & (df2['零售金额同期']>0),'是','否')
df2 = df2[['星期几(星期五) ','新主门店识别编码','是否可比店']]
week_compare = week_compare.merge(df2,on=['星期几(星期五) ','新主门店识别编码'], how='left')
week_compare_df = week_compare.loc[((week_compare['年份周(20161)'] == 201951) | (week_compare['年份周(20161)'] == 201851)) & (week_compare['是否可比店'] == '是')].copy()


compare_now_week = compare_rate('周', week_compare_df)


# 计算月可比，选取不同年份的同周数据
month_compare_df = compare_df.loc[((compare_df['年份月份 (201601)'] == 201912) | (compare_df['年份月份 (201601)'] == 201812)) & (compare_df['是否是可比店'] == '是')].copy()
compare_now_month = compare_rate('月', month_compare_df)

# 计算月可比，选取不同年份的同周数据
choose_condition = ((compare_df['年份月份 (201601)'] >= l_month_b) | (compare_df['年份月份 (201601)'] >= month_b))
quarter_compare_df = compare_df.loc[choose_condition & (compare_df['是否是可比店'] == '是')]
compare_now_quarter = compare_rate('季度', quarter_compare_df)


# ### 最早零售时间分别计算中类、小类和到大区的
# 最早零售时间，到大区、中类、小类、款号
earlist_df = pd.read_csv(r"{}\{}\earlist_sales.csv".format(base_dir, date_n), skiprows=28, dtype={'款号': str})

earlist_df = earlist_df.merge(config_where_df, on=['销售地区名称', '营销区域名称'])
earlist_df = earlist_df.merge(config_gender_df, on=['性别'])

earlist_df['日历天'] = earlist_df['日历天'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
earlist_day = earlist_df.groupby(['款号'])['日历天'].agg(lambda x: x.max()- x.min()).reset_index()
earlist_day.columns = ['款号', '时差']
earlist_day['时差'] = earlist_day['时差'].dt.days
earlist_df = earlist_df.merge(earlist_day, on=['款号'])


region_avg_sale_day = earlist_df.groupby(['渠道', '大区']).agg({'时差': 'sum', '款号': 'count'})
region_avg_sale_day['平均销售天数'] = region_avg_sale_day['时差']/region_avg_sale_day['款号']
region_avg_sale_day.columns = ['时差和', '款数和', '平均销售天数']

senior_avg_sale_day = earlist_df.groupby(['新性别', '中类', '小类']).agg({'时差': 'sum', '款号': 'count'})
senior_avg_sale_day['平均销售天数'] = senior_avg_sale_day['时差']/senior_avg_sale_day['款号']
senior_avg_sale_day.reset_index(inplace=True)


# ## 数据整合，将不同板块计算的数据合并
senior_avg_sale_day.to_excel('{}\{}\中小类平均销售天数--{}.xlsx'.format(base_dir, date_n, week_n))
result_2019_df = pd.concat([stock_sum_2019_df, allotment_2019, sales_week_2019, compare_now_week, S78_sales_week_2019, profit_week_2019_df, sales_month_2019, profit_2019_month_df, sales_quarter_2019,
                            compare_now_month, S78_sales_quarter_2019, profit_2019_quarter_df, compare_now_quarter, new_stock_2019, sale_weeks_df, avg_sales_2019, region_avg_sale_day], axis=1, sort=True)
final_2019 = result_2019_df.stack().reset_index()
final_2019.columns = ['渠道', '大区', '指标', '值']
final_2019['年份'] = 2019
# result_2019_df.to_excel(f'd:\\test\\19年sop周报-{week_n}.xlsx')


app = xw.App(visible=False, add_book=False)
xb = app.books.open(r"{}\{}\S&OP周报渠道面.xlsx".format(base_dir, date_n))

xb.sheets('19年').range('c2').value = result_2019_df.values

xb.save(r"{}\{}\S&OP周报渠道面--{}.xlsx".format(base_dir, date_n, week_n))

xb.close()
app.quit()
xw.App.kill(app)

