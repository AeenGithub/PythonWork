# -*- coding: utf-8 -*-
import json

import requests

lst_city = ['武汉','北京','上海','广州','深圳','成都','长沙','广州','重庆']
def getpois(city):   
    num = 1
    url_api = r'http://restapi.amap.com/v3/place/text'
    pois_all = [] 
    while num <= 20:
        city_name = city
        num_page = num
        dic = {'key':'a116cd29b51b3e642af47a866dd35076',
               'keywords':'广顺北大街31号院夏都家园3号楼',
               'city':city_name,
               'offset':'20',
               'output':'json',
               'extensions':'all',
               'page':num_page
              }
        try:
            req = requests.get(url_api,params=dic)
            json_one = json.loads(req.text)
            pois = json_one['pois']
        except IndexError as e:
            print('except', e)
        finally:
            pois = json_one['pois']
            pois_all.append(pois)
        num = num + 1
    return pois_all
def getgps(pois):
    count = 0
    lst_res = []
    while count <= 19:
        lst_just = []
        name = pois[count]['name']
        lng, lat = pois[count]['location'].split(',')
        address = pois[count]['address']
        lst_just = [name, lng, lat, address]
        lst_res.append(lst_just)
        count = count + 1
    for one in lst_res:
        print(one[0], one[1], one[2], one[3])
#         lnglat = cur.execute("INSERT INTO `链家`.`链家` (`name`, `lng`, `lat`, `address`) VALUES ('%s', '%s', '%s', '%s')" %(one[0], one[1], one[2], one[3]))
#         conn.commit()
#     return 'all is ok'
for city_one in lst_city:
    print(lst_city.index(city_one))
    pois_ALL = getpois(city_one)
    for pois_one in pois_ALL:
        if bool(pois_one) is True:
            try:
                getgps(pois_one)
            except IndexError as e:
                print('IndexError')
# conn.close()





