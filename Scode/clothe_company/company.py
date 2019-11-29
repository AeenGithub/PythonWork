# -*- coding: utf-8 -*-
"""
Created on Wed May 30 23:36:22 2018

@author: S103878
"""

import json
import random
import time

import pandas as pd
import requests

df = pd.read_csv(r"C:\Users\S103878\Downloads\AMap_adcode_citycode.xlsx\AMap_adcode_citycode.csv", index_col='中文名', encoding='gbk', dtype='str')
all_city_info = df.transpose().to_dict()
with open('d:\\ips.txt', 'r', encoding='utf-8') as f:
    file = f.read()
    lst_file = file.split('\n')

lst_headers = [  
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},  
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},  
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},  
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},  
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},  
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ] 


def get_one_location(words, querys, adcode):
    init_url = r'https://ditu.amap.com/search'
    init_dic = {'query': querys}
    location_url = r'https://ditu.amap.com/service/poiInfo'
    headers = random.choice(lst_headers)
    proxy = '120.76.231.27:3128'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy}
    location_dic = {'query_type': 'TQUERY',
                'pagesize': '200',
                'pagenum': '1',
                'qii': 'true',
                'cluster_state': '5',
                'need_utd': 'true',
                'utd_sceneid': '1000',
                'div': 'PC1000',
                'addr_poi_merge': 'true',
                'is_classify': 'true',
                'zoom': '12',
                'geoobj': geoobjs,
                'city': citycode,
                'keywords': words
                }
    time.sleep(30)
    with requests.Session() as s:
        s.get(init_url, params=init_dic, headers=headers, proxies=proxies)
        location_data = s.get(location_url, params=location_dic, headers=headers, proxies=proxies)
        lst_location = location_data.text 
    return json.loads(lst_location)

all_longt_lat = []
x = 1
for city in all_city_info:
    time.sleep(5)
    longtitude = all_city_info[city]['经度']
    latitude =  all_city_info[city]['纬度']
    citycode = str(all_city_info[city]['citycode'])
    words = ''.join([city, ' 以纯'])
    querys = ''.join([city, '+以纯'])
    print(x, querys)
    geoobjs = longtitude + '|' + latitude + '|' + str(float(longtitude)+0.09) + '|' + str(float(latitude)+0.09)
    try:
        json_location = get_one_location(words, querys, citycode)
        for i in json_location['data']['poi_list']:
            name = i['disp_name']
            longtitude = i['longitude']
            latitude = i['latitude']
            all_longt_lat.append([querys, name, longtitude, latitude])
            with open('d:\\city_lglat.txt', 'a', encoding='utf-8') as f:
                f.write(querys+' ' +name+' '+longtitude+' ' +latitude+'\n')
        print(len(all_longt_lat))
    except Exception as e:
        print(e)
        continue
    x += 1
with open('d:\\city_lglat_2.txt', 'w', encoding='utf-8') as f:
    f.write(str(all_longt_lat))
print(len(all_longt_lat))
print('all is ok!')