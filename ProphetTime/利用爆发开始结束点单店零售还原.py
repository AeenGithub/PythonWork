#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import stats

warnings.simplefilter(action='ignore', category=FutureWarning)
from fbprophet import Prophet
import os

time_f = pd.read_pickle(r"D:\Python\ProphetTime\configFile\store_market_time_begin_end_points_china.pickle")
time_df = time_f.copy()
time_df.head()
little_month = [4, 6, 9, 11]
time_df.loc[(time_df['开始月份'].isin(little_month)) & (time_df['开始日期'] >= 31), '开始日期'] = 30
time_df.loc[(time_df['开始月份'] == 2) & (time_df['开始日期'] >= 29), '开始日期'] = 28

time_df.loc[(time_df['结束月份'].isin(little_month)) & (time_df['结束日期'] >= 31), '结束日期'] = 30
time_df.loc[(time_df['结束月份'] == 2) & (time_df['结束日期'] >= 29), '结束日期'] = 28

# 利用prophet模型预测每个中类的未来销量
f = pd.read_pickle(r"D:/Jupyter/零售还原/单店模拟还原/指定门店筛选_2019-07-24_14-05-22.pickle")
df = f.copy()
df['日历天'] = df['日历天'].astype('str')
df['日历天'] = df['日历天'].str.replace('-', '')
df['time'] = df['日历天'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
df['year'] = df['time'].apply(lambda x: x.year)
df['month'] = df['time'].apply(lambda x: x.month)
df['days'] = df['time'].apply(lambda x: x.day)
df['周次'] = df['年周'].apply(lambda x: str(x)[-2:] if isinstance(x, int) else x)


def inverse_boxcox(y, lambda_):
    return np.exp(y) if lambda_ == 0 else np.exp(np.log(lambda_ * y + 1) / lambda_)

def calculate_forecast_errors(df, prediction_size):
    df = df.copy()
    df['e'] = df['y'] - df['yhat']
    df['p'] = 100 * df['e'] / df['y']
    predicted_part = df[-prediction_size:]
    error_mean = lambda error_name: np.mean(np.abs(predicted_part[error_name]))
    return {'MAPE': error_mean('p'), 'MAE': error_mean('e')}

def cumsum_money_95percent(main_store_num):
    # 计算一家门店零售金额累计占比达到95%的所有中类清单
    one_store = df.loc[(df['主门店识别编码'] == main_store_num)].copy()
    new2 = one_store.groupby(['中类'])['本期零售金额'].sum()
    new2 = new2.reset_index()
    new2.sort_values(by='本期零售金额', ascending=False, inplace=True)
    new2['本期零售金额占比'] = new2['本期零售金额'] / new2['本期零售金额'].sum()
    new2.sort_values(by=['本期零售金额'], ascending=False, inplace=True)
    new2['本期零售金额累计占比'] = new2['本期零售金额占比'].cumsum()

    new3 = new2.loc[new2['本期零售金额累计占比'] <= 0.95]
    return new3['中类'].tolist()

def can_use_main_store_id():
    # 筛选数据连续性强，数据年份多的门店
    group_a = df.groupby(['主门店识别编码', 'year'])['time'].nunique()
    group_a.name = 'count'
    group_b = group_a.reset_index()
    group_c = group_b.groupby(['主门店识别编码'])['year'].count()
    # 挑选年份计数小于等于2年的门店
    cccc = set(group_c[group_c <=2].index.tolist())
    # 挑选半年内没有零售的门店
    group_b = group_b[group_b['year'] <= 2018]
    aaaa = set(df['主门店识别编码'].unique().tolist())
    bbbb = set(group_b.loc[group_b['count'] <= 180, '主门店识别编码'].tolist())
    # 挑选出销售时间间隔大于30天的门店，即30天内没有任何零售的门店
    group_d = df.groupby(['主门店识别编码', 'year', 'time'])['time'].nunique()
    group_d.name = 'count'
    group_e = group_d.reset_index()
    group_e['day_div'] = (group_e['time']- group_e['time'].shift(1)).dt.days
    group_e['year_div'] = (group_e['year']- group_e['year'].shift(1))
    less_thirty_days = set(group_e.loc[(group_e['day_div'] > 30) & (group_e['year_div'] == 0), '主门店识别编码'].tolist())
    # 删除所有不需要的门店
    can_use_store = aaaa.difference(bbbb).difference(cccc).difference(less_thirty_days)
    return list(can_use_store)

def one_senior_data_clean(main_store_num, one_senior):
    '''通过一个门店一个中类的数据，寻找到有效的数据，防止部分品类部分年份数据缺失严重，无法使用'''
    # 目前解决了临近2018年的销售数据缺失问题，但是未能解决中间值缺失问题
    one_store = df.loc[(df['主门店识别编码'] == main_store_num) & (df['中类'] == one_senior)].copy()
    year_choose = one_store.groupby(['year'])['time'].count()
    # 设定阈值,每一年销售总天数最多的值,除以np.e才能得到最小有效数据年份的阈值
    threshold = year_choose.max() / np.e
    need_years = year_choose[year_choose >= threshold].index
    # need_years = need_years.sort_values(ascending=False)
    one_store = one_store[one_store['year'].isin(need_years)].copy()
    # 当最大数值小于2018时，整体偏移，但是中间值出现缺失，怎么办
    if one_store['time'].max().year <= 2018:
        div_days = pd.datetime(2018, one_store['time'].max().month, one_store['time'].max().day) - one_store['time'].max()
        one_store['time'] = one_store['time'] + div_days
    one_store['本期零售金额'].fillna(value=0, inplace=True)
    one_store.loc[one_store['本期零售金额'] < 0, '本期零售金额'] = 0
    copy_store = one_store[['本期零售金额', 'time']].copy()
    return (one_store, copy_store)

def get_time_delta():
    years_lst = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    bg_month, bg_day, ed_month, ed_day = time_begin_end.values[0]
    for only_year in years_lst:
        if ed_month > bg_month:
            bg_time = pd.Timestamp(only_year, bg_month, bg_day)
            ed_time = pd.Timestamp(only_year, ed_month, ed_day)
        else:
            bg_time = pd.Timestamp(only_year, bg_month, bg_day)
            ed_time = pd.Timestamp(only_year+1, ed_month, ed_day)
        yield (bg_time, ed_time)


can_use_store = can_use_main_store_id()
for main_store_num in can_use_store:
    # main_store_num = can_use_store[1]
    if os.path.exists(main_store_num):
        print('{}已经存在'.format(main_store_num))
    else:
        os.mkdir(main_store_num)
    percent_up_95 = cumsum_money_95percent(main_store_num)
    for one_senior in percent_up_95:
        one_store, copy_store = one_senior_data_clean(main_store_num, one_senior)
        box_cox_data, lambda_ = stats.boxcox(copy_store['本期零售金额'] + 1)
        copy_store['new_money'] = box_cox_data
        copy_store2018 = copy_store.loc[copy_store['time'].dt.year <= 2018].copy()

        time_begin_end = time_df.loc[(time_df['主门店识别码'] == main_store_num) & (time_df['中类'] == one_senior), ['开始月份', '开始日期', '结束月份', '结束日期']]
        if time_begin_end.empty:
            break
        else:
            get_time_delta_lst = list(get_time_delta())
        years_lst = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

        def deal_timedetla(one_time_df):
            # 循环每一年，结合开始点和结束点，筛选数据并合并汇总处理
            total_phet_data_lst = []
            for index, only_year in enumerate(years_lst):
                bg_time, ed_time = get_time_delta_lst[index]
                mask_phet_2 = ((one_time_df['time'] >= bg_time) & (one_time_df['time'] <= ed_time) & (one_time_df['time'].dt.year <= only_year+1))
                one_phet_data = one_time_df.loc[mask_phet_2]
                total_phet_data_lst.append(one_phet_data)
            result_data = pd.concat(total_phet_data_lst, sort=True, ignore_index=True)
            return result_data

        # 根据prophet的数据重新设置数据的时间范围
        phet_data = deal_timedetla(copy_store2018)
        phet_data.rename({'new_money': 'y', 'time': 'ds', '本期零售金额': 'money'}, axis=1, inplace=True)
        phet_data = phet_data[['ds', 'y']]
        # 市场预期设置阈值
        cap = phet_data['y'].mean()
        phet_data['cap'] = 5.5

        m = Prophet(
                    growth='logistic',
                    changepoint_prior_scale=5,
                    daily_seasonality=False,
                    weekly_seasonality=200,
                    yearly_seasonality=10,
                    holidays_prior_scale=100,
                   )
        m.add_country_holidays(country_name='CN')
        fit_m = m.fit(phet_data)
        future = fit_m.make_future_dataframe(periods=365, freq='D')
        future['cap'] = 5.5 * 0.9
        future['time'] = future['ds']
        # 对数据异常区域删除
        future2 = deal_timedetla(future)
        forecast = fit_m.predict(future2)

        one_store = one_store[['本期零售金额', 'time']].copy()
        result_data = one_store.merge(forecast[['ds', 'yhat']], left_on='time', right_on='ds', how='outer')
        result_data.rename(columns={'本期零售金额': 'y'}, inplace=True)
        result_data['y'].replace(0, result_data['y'].mean(), inplace=True)
        result_data['预测零售金额'] = result_data['yhat'].apply(lambda x: inverse_boxcox(x, lambda_))
        result_data['中类'] = one_senior
        result_data = result_data[['time', 'y', '预测零售金额', 'ds', '中类']]
        result_data.to_excel('{}/{}的预测.xlsx'.format(main_store_num, one_senior))

# calculate_forecast_errors(result_data, 100)
# result_data.iplot(x='time', y=['y', 'yhat'], filename='aaa', asPlot=True)
# In[ ]:



