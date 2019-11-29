import csv
import json
import os
import random
import time

import pandas as pd
import requests


class location_around(object):
    def __init__(self, shopcenter_link, headers):
        self.shopcenter_link = shopcenter_link
        self.headers = headers
        self.base_dir = os.getcwd()

    def file_read(self):
        """购物中心数据读取"""
        df = pd.read_csv(self.shopcenter_link, sep='\t')
        file_content = df.reset_index().values
        total_lines = len(file_content)
        with open(r'{}\already_download.csv'.format(self.base_dir), 'a', newline='', encoding='utf-8') as f:
            pass
        with open(r'{}\already_download.csv'.format(self.base_dir), 'r', newline='') as f:
            linenum = len(f.readlines())
        print('------csv文件共有{}个购物中心------'.format(len(file_content)))
        if linenum == 0:
            pass
        elif linenum > 0 and linenum < total_lines:
            print("由于上次下载中断，继续访问剩余{}个购物中心".format(
                len(pd.read_csv(self.shopcenter_link, skiprows=linenum).values)))
        else:
            print("下载完成")
        file2_content = pd.read_csv(self.shopcenter_link)
        file2_content = file2_content.reset_index().values
        return file2_content

    def log(self, data):
        """请求失败的购物中心数据保存至日志，以待重新爬取"""
        with open(r'{}\log.csv'.format(self.base_dir), mode='a+', newline='') as f:
            content_writer = csv.writer(f)
            content_writer.writerow(data)
        return ''

    def url_internet(self, one_row):
        """请求网络数据"""
        seqq, formatted_address, country, province, citycode, city, district, adcode, lng, lat, name_store = one_row					
        # poiid, name_store, types, address, lng, lat, province_name, city_name, county_name, city = one_row
        try:
            url1 = 'https://restapi.amap.com/v3/place/around?key=38223614c364192a208aa2bc3d4b2e74&location={},{}&types=141201&radius=1000&offset=20&page=1&extensions=all'.format(
                lng, lat)
            time.sleep(random.uniform(0.1, 0.3))
            print("数据中心：{} 经纬度：{}, {} 辐射半径：1kM 正在访问".format(name_store, lng, lat))
            res = requests.get(url=url1, headers=headers).text
            res_json = json.loads(res)
            count = res_json.get('count')
            pagenums = (int(count) // 20) + 2
            print(
                "数据中心：{} 经纬度：{}, {} 辐射半径：1kM 共有{}页数据".format(name_store, lng, lat, pagenums - 1))
            for pagenum in range(0, pagenums):
                url1 = 'https://restapi.amap.com/v3/place/around?key=38223614c364192a208aa2bc3d4b2e74&location={},{}&types=141201&radius=1000&offset=20&page={}&extensions=all'.format(
                    lng, lat, pagenum)
                time.sleep(random.uniform(0.1, 0.2))
                print(
                    "\t------数据中心：{} 经纬度：{}, {} 辐射半径：1kM  {}页数据正在访问------".format(name_store, lng, lat, pagenum))
                res = requests.get(url=url1, headers=headers).text
                res_json = json.loads(res)
                pois = res_json.get('pois')
                for poi in pois:
                    poiid2 = poi.get('id')
                    name2 = poi.get('name')
                    types = poi.get('type')
                    typecode = poi.get('typecode')
                    address = poi.get('address')
                    location = poi.get('location')
                    pcode = poi.get('pcode')
                    pname = poi.get('pname')
                    citycode = poi.get('citycode')
                    cityname = poi.get('cityname')
                    adcode = poi.get('adcode')
                    adname = poi.get('adname')
                    indoor_map = poi.get('indoor_map')
                    indoor_data = poi.get('indoor_data')
                    # if indoor_map != '0':
                    floor = indoor_data.get('floor')
                    truefloor = indoor_data.get('truefloor')
                    content = [
                        formatted_address,
                        name_store,
                        poiid2,
                        name2,
                        types,
                        typecode,
                        address,
                        pname,
                        pcode,
                        cityname,
                        citycode,
                        adname,
                        adcode,
                        indoor_map,
                        location,
                        indoor_data,
                        floor,
                        truefloor,
                    ]
                    with open(r'{}\semir_location_around_1000.csv'.format(self.base_dir), 'a', newline='') as f:
                        content_writer = csv.writer(f)
                        content_writer.writerow(content)
                print(
                    "\t购物中心：{} 经纬度：{}, {} 辐射半径：1kM  {}页数据保存完成".format(name_store, lng, lat, pagenum))
            print('{}数据保存完成'.format(name_store))
        except Exception as e:
            self.log(one_row)
            print("{}网络请求失败，请求失败的数据已保存至本地".format(name_store))
        with open(r'{}\already_download.csv'.format(self.base_dir), 'a', newline='') as f:
            already_download = csv.writer(f)
            already_download.writerow(one_row)

    def main(self):
        for one_row in self.file_read():
            self.url_internet(one_row)


if __name__ == '__main__':
    shopcenter_link = r'D:\Python\TmallCrawler\SEMIR_REAL_ADDRESS.csv'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3702.0 Safari/537.36'
    }
    gf = location_around(shopcenter_link, headers)
    gf.main()
