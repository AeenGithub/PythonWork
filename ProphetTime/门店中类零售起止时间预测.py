# coding: utf-8

# In[431]:


import warnings
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import signal
from scipy import stats

warnings.simplefilter(action='ignore', category=FutureWarning)

def inverse_boxcox(y, lambda_):
    # 逆向反转box_cox函数
    return np.exp(y) if lambda_ == 0 else np.exp(np.log(lambda_ * y + 1) / lambda_)

def calculate_forecast_errors(df, prediction_size):
    # 计算准确率和误差率
    df = df.copy()
    df['e'] = df['y'] - df['yhat']
    df['p'] = 100 * df['e'] / df['y']
    predicted_part = df[-prediction_size:]
    error_mean = lambda error_name: np.mean(np.abs(predicted_part[error_name]))
    return {'MAPE': error_mean('p'), 'MAE': error_mean('e')}

f = pd.read_pickle(r"D:/Jupyter/零售还原/单店模拟还原/指定门店还原模型_2019-07-09_18-38-32.pickle")
df = f.copy()
df['日历天'] = df['日历天'].astype('str')
df['日历天'] = df['日历天'].str.replace('-', '')
df['time'] = df['日历天'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
df['year'] = df['time'].apply(lambda x: x.year)
df['month'] = df['time'].apply(lambda x: x.month)
df['days'] = df['time'].apply(lambda x: x.day)
df['周次'] = df['年周'].apply(lambda x: str(x)[-2:] if isinstance(x, int) else x)

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

def get_bg_ed(main_store_num, one_senior):
    one_store = df.loc[(df['主门店识别编码'] == main_store_num) & (df['中类'] == one_senior)].copy()
    one_store.loc[one_store['本期零售金额'] < 0, '本期零售金额'] = 0
    one_store['本期零售金额'].fillna(value=0, inplace=True)
    copy_store = one_store[['本期零售金额', 'time']].copy()
    # 这里经常出现无法接受到两个值的情况，是否考虑改到df上去
    box_cox_data, lambda_ = stats.boxcox(copy_store['本期零售金额'] + 1)
    copy_store['new_money'] = box_cox_data
    copy_store2018 = copy_store.loc[copy_store['time'].dt.year <= 2018].copy()
    copy_store2018.index = range(copy_store2018.shape[0])

    copy_store2018['new_money2'] = copy_store2018['new_money'] - copy_store2018['new_money'].shift(7)
    copy_store2018['new_money2'].fillna(copy_store2018['new_money2'].mean(), inplace=True)
    index_less = signal.argrelextrema(copy_store2018['new_money2'].values, np.less)[0].tolist()
    if index_less:
        index_less_df = copy_store2018.loc[index_less].copy()
        index_less_df.index = range(len(index_less_df))
        index_less_df = index_less_df.loc[index_less_df['new_money'] >0 ].copy()
        index_less_df['year'] = index_less_df['time'].dt.year

        # 计算当前日期与前一天日期的天数差
        index_less_df['days_div1'] = (index_less_df['time'] - index_less_df['time'].shift(1))
        index_less_df['days_div1'] = index_less_df['days_div1'].dt.days

        # 计算当前日期与后一天日期的天数差
        index_less_df['days_div2'] = index_less_df['time'].shift(-1) - index_less_df['time']
        index_less_df['days_div2'] = index_less_df['days_div2'].dt.days

        # 计算当前日期与前一天日期的销售额差
        index_less_df['ratio1'] = (index_less_df['new_money'] - index_less_df['new_money'].shift(1))/index_less_df['days_div1']
        # 计算当前日期与后一天日期的销售额差
        index_less_df['ratio2'] = (index_less_df['new_money'].shift(-1) - index_less_df['new_money'])/index_less_df['days_div2']
        # 如果筛选出来的极值点的季度里，缺少某一个季度，那么该季度就是需要的季度，如果四个季度都存在，那么季度零售额排名，并计算累计占比，如果占比小于0.05，则该季度就是我们需要的季度
        # 不同品类选取的范围是否可以提前输入，羽绒服。0.001， 毛衫0.05
        index_less_df2 = index_less_df.loc[(index_less_df['ratio1'] < 0 ) & (index_less_df['ratio2'] > 0)].copy()
        index_less_df2.loc[(index_less_df2['time'].dt.month <= 2) | (index_less_df2['time'].dt.month == 12), 'quarter'] = '冬'
        index_less_df2.loc[(index_less_df2['time'].dt.month <= 5) & (index_less_df2['quarter'].isnull()), 'quarter'] = '春'
        index_less_df2.loc[(index_less_df2['time'].dt.month <= 8) & (index_less_df2['quarter'].isnull()), 'quarter'] = '夏'
        index_less_df2.loc[(index_less_df2['time'].dt.month <= 11) & (index_less_df2['quarter'].isnull()), 'quarter'] = '秋'

        quarter_sum = index_less_df2.groupby(['quarter'])['本期零售金额'].sum()
        quarter_sum = quarter_sum.reset_index()
        quarter_sum.sort_values(by=['本期零售金额'], ascending=False, inplace=True)
        quarter_sum['cumsum'] = quarter_sum['本期零售金额'].cumsum()
        quarter_sum['cumsum_rete'] = quarter_sum['cumsum'] / quarter_sum['本期零售金额'].sum()
        quarter_sum['rate'] = quarter_sum['本期零售金额'] / quarter_sum['本期零售金额'].sum()
        # quarter里可能只有一个季节，两个季节，也有可能三个季节，四个季节
        quarter_name = {'冬', '春', '夏', '秋'}
        quarter_count = len(set(quarter_sum['quarter'].tolist()))
        if quarter_count >= 2:
            no_data_quarter = quarter_name.difference(set(quarter_sum['quarter'].tolist()))
            no_data_quarter_005 = quarter_sum.loc[quarter_sum['rate'] <= 0.01]['quarter']
            if no_data_quarter:
                no_data_quarter_name = list(no_data_quarter)[0]
            elif no_data_quarter_005.empty is False:
                no_data_quarter_name = quarter_sum.loc[quarter_sum['rate'] <= 0.01]['quarter'].values[0]
            else:
                no_data_quarter_name = None

            if no_data_quarter_name == '夏':
                index_less_df_begin = index_less_df2.loc[(index_less_df2['days_div1'] <= 30.25) & (index_less_df2['time'].dt.month > 6)].copy()
                begin_time_points = index_less_df_begin.groupby('year')['time'].min()
                index_less_df_end = index_less_df2.loc[(index_less_df2['days_div2'] <= 30.25) & (index_less_df2['time'].dt.month <= 6)].copy()
                end_time_points = index_less_df_end.groupby('year')['time'].max()
            else:
                index_less_df_begin = index_less_df2.loc[(index_less_df2['days_div1'] <= 30.25)].copy()
                begin_time_points = index_less_df_begin.groupby('year')['time'].min()
                index_less_df_end = index_less_df2.loc[(index_less_df2['days_div2'] <= 30.25)].copy()
                end_time_points = index_less_df_end.groupby('year')['time'].max()
        else:
            only_one_quarter = set(quarter_sum['quarter'].tolist())
            if only_one_quarter == '夏':
                index_less_df_begin = index_less_df2.loc[(index_less_df2['days_div1'] <= 30.25)].copy()
                begin_time_points = index_less_df_begin.groupby('year')['time'].min()
                index_less_df_end = index_less_df2.loc[(index_less_df2['days_div2'] <= 30.25)].copy()
                end_time_points = index_less_df_end.groupby('year')['time'].max()
            else:
                index_less_df_begin = index_less_df2.loc[(index_less_df2['days_div1'] <= 30.25) & (index_less_df2['time'].dt.month > 6)].copy()
                begin_time_points = index_less_df_begin.groupby('year')['time'].min()
                index_less_df_end = index_less_df2.loc[(index_less_df2['days_div2'] <= 30.25) & (index_less_df2['time'].dt.month <= 6)].copy()
                end_time_points = index_less_df_end.groupby('year')['time'].max()

        bg_month = [begin_time_points[i].month for i in begin_time_points.index]
        bg_day = [begin_time_points[i].day for i in begin_time_points.index]
        ed_month = [end_time_points[i].month for i in end_time_points.index]
        ed_day = [end_time_points[i].day for i in end_time_points.index]
        bg_day_res = np.min(bg_day)
        bg_month_res = np.min(bg_month)
        # 求最大值的地方，有的时候没有最大值
        ed_day_res = np.max(ed_day)
        ed_month_res = np.max(ed_month)
    else:
        bg_month_res, bg_day_res, ed_month_res, ed_day_res = 1, 1, 12, 31
    return (bg_month_res, bg_day_res, ed_month_res, ed_day_res)

def main():
    result_lst = []
    can_use_store = can_use_main_store_id()
    for main_store_num in can_use_store:
        percent_up_95 = cumsum_money_95percent(main_store_num)
        for one_senior in percent_up_95:
            print(f'{main_store_num}--{one_senior}正在运行中……')
            try:
                bg_month_res, bg_day_res, ed_month_res, ed_day_res = get_bg_ed(main_store_num, one_senior)
            except ValueError as e:
                print('该品类零售额和数据记录过低，出现异常', e.args)
                continue
            result_lst.append((main_store_num, one_senior, bg_month_res, bg_day_res, ed_month_res, ed_day_res))
            print(main_store_num, '--', one_senior, '售卖起始： {}月{}日--{}月{}日\n'.format(bg_month_res, bg_day_res, ed_month_res, ed_day_res))
    result_df = pd.DataFrame(result_lst)
    result_df.columns = ['主门店识别码', '中类', '开始月份', '开始日期', '结束月份', '结束日期']
    result_df.to_excel('d:\\test\\上海门店的各个中类的上下市时间.xlsx', index=False)
    result_df.to_pickle('store_market_time_begin_end_points.pickle')


if __name__ == '__main__':
    main()

# phet_time_bg = pd.datetime(2000, bg_month_res, bg_day_res)
# phet_time_ed = pd.datetime(2000, ed_month_res, ed_day_res)
#
#
# copy_store['new_time'] = copy_store['time'].apply(lambda x: pd.datetime(2000, x.month, x.day))
#
# mask_phet_2 = ((copy_store['new_time'] >= phet_time_bg) & (copy_store['new_time'] <= phet_time_ed) &
#                (copy_store['time'].dt.year <= 2018))
# # 根据prophet的数据重新设置数据格式和名称
# phet_data = copy_store.loc[(copy_store['time'].dt.year <= 2018) , ['time', 'new_money']].copy()
# phet_data.columns = ['ds', 'y']
#
# # 市场预期设置阈值
# cap = phet_data['y'].mean()
# phet_data['cap'] = 6
#
# m = Prophet(
#             growth='logistic',
#             changepoint_prior_scale=5,
#             daily_seasonality=False,
#             weekly_seasonality=200,
#             yearly_seasonality=20,
#             holidays_prior_scale=100,
#            )
# m.add_country_holidays(country_name='CN')
# m.fit(phet_data)
#
# future = m.make_future_dataframe(periods=365, freq='D')
# future['cap'] = 6 * 0.9
# future['new_time'] = future['ds'].apply(lambda x: pd.datetime(2000, x.month, x.day))
# mask = (future['new_time'] >= phet_time_bg) & (future['new_time'] <= phet_time_ed)
# future2 = future.loc[mask]
# forecast = m.predict(future2)
#
#
# x1 = forecast['ds']
# y1 = forecast['yhat']
#
# fig, ax = plt.subplots(figsize=(20, 8))
# ax.spines['top'].set_color('white')
# ax.spines['right'].set_color('white')
#
# plt.ylim(-1,50)
# plt.xlim(datetime(2017,1,1), datetime(2019,10,1))
# plt.plot(copy_store['time'], copy_store['new_money'],c='r')
# plt.plot(x1, y1, c='y')
# plt.show()
#
#
# # In[3203]:
#
#
# result_data = copy_store.merge(forecast[['ds', 'yhat']], left_on='time', right_on='ds')
#
#
# # In[3204]:
#
#
# result_data.rename(columns={'本期零售金额': 'y'},inplace=True)
#
#
# # In[3205]:
#
#
# result_data['y'].replace(0, result_data['y'].mean(), inplace=True)
#
#
# # In[3206]:
#
#
# result_data['yhat'] = result_data['yhat'].apply(lambda x: inverse_boxcox(x, lambda_))
#
#
# # In[3207]:
#
#
# calculate_forecast_errors(result_data, 100)
#
#
# # In[3208]:
#
#
# # forecast.iloc[-100:, :]
#
#
# # In[3209]:
#
#
# result_data.iplot(x='time', y=['y', 'yhat'])
#
#
# # In[3210]:
#
#
# from fbprophet.diagnostics import cross_validation
# from fbprophet.diagnostics import performance_metrics
# from fbprophet.plot import plot_cross_validation_metric
#
#
# # In[3216]:
#
#
# df_cv = cross_validation(m, period='180 days', horizon = '180 days')
#
#
# # In[3212]:
#
#
# performance_metrics(df_cv)
#
#
# # In[3215]:
#
#
# plot_cross_validation_metric(df_cv, metric='rmse')
# plt.show()
#
#
# # In[ ]:
#
#
#
#
