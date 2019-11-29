# -*- coding: utf-8 -*-
"""
Created on Wed May 30 23:23:22 2018

@author: S103878
"""

import requests

# all url
init_url = r'https://ditu.amap.com/search'
get_citydata_url = r'https://ditu.amap.com/service/cityList'
init_dic = {'query': '厦门+以纯'}
get_citydata_url_dic = {'version': ''}
with requests.Session() as s:
    init_res = s.get(init_url, params=init_dic)
    get_citydata = s.get(get_citydata_url, params=get_citydata_url_dic)
    city_file = get_citydata.text
with open('d:\\city_lglat.txt', 'w', encoding='utf-8') as f:
    f.write(city_file)
    print('ok')
with open('d:\\city_lglat.txt', 'w', encoding='utf-8') as f:
    f.write(city_file)
    print('ok')
