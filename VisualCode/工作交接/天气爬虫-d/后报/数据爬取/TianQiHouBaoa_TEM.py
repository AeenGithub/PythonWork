# -*- coding:utf-8 -*-
import os
import re
import sqlite3 as mysql
import urllib.request as brequest
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
from lxml import etree
from retrying import retry


def get_name(url_name):
    return url_name.split("/")[1].split(".")[0]

def get_city_name(url_city):
    '''获取当前所有的城市列表'''
    base_url = "http://www.tianqihoubao.com"
    city_url = urlparse.urljoin(base_url, url_city)
    # print city_url
    html = requests.get(city_url).content
    html_tree = etree.HTML(html)
    links = html_tree.xpath("//td//a/@href")
    return map(get_name, links)

def get_citys_name(urls_citys):
    rongqi_dict = OrderedDict()
    rongqi_list = list()
    rongqi = dict()
    for city in urls_citys:
        temp = get_city_name(city)
        rongqi_dict[city] = temp
        rongqi_list.extend(temp)
    rongqi['rongqi_dict'] = rongqi_dict
    rongqi['rongqi_list'] = rongqi_list
    return rongqi

@retry(stop_max_attempt_number=3, wait_random_min=100, wait_random_max=2000)
def parser_html(url, path):
    '''解析当前链接的网页并保存到本地'''
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    request_url = brequest.Request(url, headers=headers)
    response = brequest.urlopen(request_url, timeout=200)
    html = response.read().decode('gbk')
    # with open(path, 'w+') as f:
    #     f.write(html)
    return html

# path
def parser_real_data_html(html):
    '''将网页中的数据解析并保存成指定格式, 结果返回两层列表'''
    html_tree = etree.HTML(html, parser=etree.HTMLParser(encoding='gbk'))
    # 这里会出错，属性错误，html——tree为none
    riqi_ori = html_tree.xpath("//tr[position()>=2]/td[1]//a/text()")
    tianqi_ori = html_tree.xpath("//tr[position()>=2]/td[2]/text()")
    qiwen_ori = html_tree.xpath("//tr[position()>=2]/td[3]/text()")
    fengxiang_ori = html_tree.xpath("//tr[position()>=2]/td[4]/text()")
    didian_lst_one = html_tree.xpath("//*[@id='content']/h1/text()")
    didian_lst = didian_lst_one * riqi_ori.__len__()
    cbind = zip(riqi_ori, tianqi_ori, qiwen_ori, fengxiang_ori, didian_lst)
    new_cbind = []
    for one_day in cbind:
        # 对数据进行简单的清洗
        one_day = [i.replace(' ', '').strip('\n').replace('\n', '*').replace('/', '') for i in one_day]
        one_day = [i.replace(' ', '').strip('\r').replace('\r', '*') for i in one_day]
        new_cbind.append(one_day)
    # 返回该城市在该月份下每一天的天气情况
    return new_cbind

def clear_real_datas(city, month_weather):
    '''对于一个月的天气数据清洗，按照数据库要求格式保存成dict，外面嵌套列表，一天一个dict，一个月一个list'''
    one_month_data = []
    for one_day_weather in month_weather:
        # 根据上个函数获得的每天的数据，进行更进一步的解析
        riqi, tianqi, qiwen, fengxiang, didian = one_day_weather
        # 将天气数据按照年月日分别处理
        match_result = re.findall('([0-9]{1,4})年([0-9]{1,2})月([0-9]{1,2})日', riqi)
        if match_result:
            year, month, day = match_result[0]
            ymd_time =  datetime.strptime('{}{}{}'.format(year, month, day), '%Y%m%d')
            ymd = datetime.strftime(ymd_time, '%Y%m%d')
            try:
                tianqi_am, tianqi_pm = [i for i in tianqi.split('*') if i != '']
            except ValueError as e:
                # 如果出现只有一个数据的，让你上午和下午均为同一个值
                tianqi_am = tianqi_pm = ''.join([i for i in tianqi.split('*') if i != ''])
            try:
                max_tm, min_tm = [i[:-1] for i in qiwen.split('*') if i != '']
            except ValueError as e:
                max_tm = min_tm = ''.join([i[:-1] for i in qiwen.split('*') if i != ''])
            try:
                ave_tm = round((int(max_tm) + int(min_tm))/2, 1)
            except ValueError as e:
                ave_tm = np.NaN
            try:
                fengxiang_t, fengli = [i for i in fengxiang.split('*') if i != '']
            except ValueError as e:
                # 如果出现只有一个数据的，让你上午和下午均为同一个值
                fengxiang_t = fengli = ''.join([i for i in fengxiang.split('*') if i != ''])
            # 获取当前的日期所在的周次和星期几
            other_year, weeknum, weekday = ymd_time.isocalendar()
            yearweek = int(datetime.strftime(ymd_time, '%Y%W'))+1
            area_name = didian.split('历史')[0]
            one_day_dict = {
                'city_ymd': '{}-{}'.format(city, ymd),
                'year': year,
                'month': month,
                'day': day,
                'ymd': ymd,
                'city': city,
                'tianqi_am': tianqi_am,
                'tianqi_pm': tianqi_pm,
                'max_tm': max_tm,
                'min_tm': min_tm,
                'fengxiang_t': fengxiang_t,
                'fengli': fengli,
                'yearweek': yearweek,
                'week': weeknum,
                'weekday': weekday,
                'ave_tm': ave_tm,
            }
            one_month_data.append(one_day_dict)
    return one_month_data

def write_insert_sql(lst_data, config_file, conn):
    '''链接数据库并将先关表格串联，写入数据库'''
    config_df = pd.read_excel(config_file)
    new_df = pd.DataFrame(lst_data)
    result_df = new_df.merge(config_df, on=['city'])
    result_df.drop_duplicates(inplace=True)
    result_df.to_sql(
        name='WeatherAll',
        con=conn,
        chunksize=1000000,
        if_exists = 'append',
        index=False,
        )
    return '所有的数据已经保存到数据库中'

if __name__ =="__main__":
    # 获取当前文件所在地址的父级目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 获得当前文件夹下所在的配置文件
    ori_file_path = r"{}\buchong2.csv".format(base_dir)
    config_file = r"{}\city_config.xls".format(base_dir)
    conn = mysql.connect(r"D:\SQLBASE\WeatherBefore.db")
    cur = conn.cursor()
    # 利用pandas读取文件中的城市列表名
    city_month_df = pd.read_csv(
        ori_file_path,
        sep=',',
        encoding='utf-8',
        dtype={'city': str, 'time': str}
    )
    # 通过日期的传入，返回城市和日期对应的字典
    city_month_df['weather_url'] = city_month_df.apply(lambda x: "http://www.tianqihoubao.com/lishi/%s/month/%s.html" % (x['city'], x['time']),axis=1)
    # city_month_df.drop(columns=['time'], inplace=True)
    # 将城市与对应链接做成字典
    # for one_city in cities_dict:
    for one_row in city_month_df.iterrows():
        # 获得一个城市下不同月份的所有链接
        real_urls = one_row[1]['weather_url']
        # for index, values in enumerate(real_urls):
        year_month = one_row[1]['time']
        one_city = one_row[1]['city']
        print('{}--{}的数据，开始写入'.format(one_city, year_month))
        city_m_html = parser_html(real_urls, '{}\\data\\{}_{}.html'.format(base_dir, one_city, year_month))
        new_cbind = parser_real_data_html(city_m_html)
        if new_cbind:
            one_month_data = clear_real_datas(one_city, new_cbind)
            try:
                write_insert_sql(one_month_data, config_file, conn)
            except mysql.IntegrityError as e:
                print('{}--{}的数据已经写过，跳过'.format(one_city, year_month), e)
                continue
            except KeyError as e:
                print('{}--{}的数据下载失败'.format(one_city, year_month), e)
                with open('{}\log'.format(base_dir), 'a+', encoding='utf-8') as f:
                    f.write('{}-{}\n'.format(one_city, year_month))
                continue
            conn.commit()
            print('{}--{}的数据，完成写入\n'.format(one_city, year_month))
        else:
            print('{}--{}的数据获取失败'.format(one_city, year_month))
            with open('{}\log'.format(base_dir), 'a+', encoding='utf-8') as f:
                    f.write('{}-{}\n'.format(one_city, year_month))
    conn.close() 
    print('all is ending')


