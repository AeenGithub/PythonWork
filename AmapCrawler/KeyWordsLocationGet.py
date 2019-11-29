#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

import csv
import json
import time
from pathlib import Path

import pandas as pd
import requests


class KeyWordsLocation(object):
    def __init__(self):
        self.url = 'https://restapi.amap.com/v3/geocode/geo'
        self.service_key = '38223614c364192a208aa2bc3d4b2e74'
        self.field_name = ['formatted_address',
                           'country',
                           'province',
                           'citycode',
                           'city',
                           'district',
                           'township',
                           'neighborhood',
                           'building',
                           'adcode',
                           'street',
                           'number',
                           'location',
                           'level',
                           'longitude',
                           'latitude',
                           'init_address',
                           'init_city']

    def request_data_map(self, address, city):
        params = {'key': self.service_key,
                  'address': address,
                  'city': city
                  }
        lng_lat_response = requests.get(self.url, params=params)
        json_data = json.loads(lng_lat_response.text)
        geocodes = json_data['geocodes']
        if geocodes:
            first_geocodes = geocodes[0]
            first_geocodes['longitude'] = first_geocodes['location'].split(',')[0]
            first_geocodes['latitude'] = first_geocodes['location'].split(',')[1]
        else:
            first_geocodes = {'longitude':'', 'latitude': ''}
        return first_geocodes


    def main(self):
        address_file = Path(r'D:\Test\semir_address.csv')
        address_df = pd.read_csv(address_file, sep='\t', header=None)
        for one_row in address_df.iterrows():
            address = one_row[1][2]
            city = one_row[1][3]
            time.sleep(0.1)
            first_geocodes = self.request_data_map(address, city)
            first_geocodes['init_address'] = address
            first_geocodes['init_city'] = city
            with open(r'D:\文档\门店动态图\门店地址经纬度查询\semir_result.csv', newline='', encoding='utf-8', mode='a+') as f:
                writer = csv.DictWriter(f, fieldnames=self.field_name)
                writer.writeheader()
                writer.writerow(first_geocodes)

if __name__ == '__main__':
    location = KeyWordsLocation()
    location.main()
    # address = '湖北省武昌区解放路439号专卖'
    # city = '武汉'
    # location.request_data_map(address, city)