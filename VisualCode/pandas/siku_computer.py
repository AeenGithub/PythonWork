#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

import pandas as pd
import requests
from bs4 import BeautifulSoup

ideage_url = 'http://search.secoo.com/search?keyword=ideage&level=0&qfs=1'

home_headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Connection': "keep-alive",
    'Cookie': "__jsluid=a7449e0f4d5ff0a516c3c98e7f07d05d; __jsl_clearance=1547028012.592|0|wK7ScEtCaG0mCxZ9dyv7YbCZV8g%3D; search_req_id=ea3b749b-aaef-4d75-a444-39583ee2b02c; BIGipServerpool_proxy=1060284608.20480.0000; gr_user_id=aa8c5786-25c8-4082-aa49-7d969729113e; ab95574fe95f2817_gr_session_id=f33db7da-0b9b-4dbb-b53c-f9b1c1e94a7d; grwng_uid=0f67989c-e1d5-4613-835c-ab99cc0ec97f; __xsptplusUT_219=1; __utma=145630134.529174038.1547027958.1547027958.1547027958.1; __utmc=145630134; __utmz=145630134.1547027958.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_UA-40733470-5=1; __utmb=145630134.2.10.1547027958; ab95574fe95f2817_gr_session_id_f33db7da-0b9b-4dbb-b53c-f9b1c1e94a7d=true; Hm_lvt_b844e792cd7084d8aae7a1d885ef5c29=1547027958; Hm_lpvt_b844e792cd7084d8aae7a1d885ef5c29=1547027958; _jzqa=1.4468574695271751000.1547027958.1547027958.1547027958.1; _jzqc=1; _jzqx=1.1547027958.1547027958.1.jzqsr=search%2Esecoo%2Ecom|jzqct=/search.-; _jzqckmp=1; __xsptplus219=219.1.1547027957.1547027957.1%234%7C%7C%7C%7C%7C%23%23APdqUgJDIrcEXclqlev9bgXu_TmhjxdN%23; _qzja=1.469524767.1547027957722.1547027957722.1547027957722.1547027957722.1547027957722.0.0.0.1.1; _qzjc=1; _qzjto=1.1.0; _jzqb=1.1.10.1547027958.1; _ga=GA1.3.529174038.1547027958; _gid=GA1.3.541065338.1547027958; _dc_gtm_UA-40733470-1=1; _qzjb=1.1547027957722.1.0.0.0; NTKF_T2D_CLIENTID=guest3858814E-24B4-88E6-AE0C-320D49C6E096; nTalk_CACHE_DATA={uid:ck_1000_ISME9754_guest3858814E-24B4-88,tid:1547027958214434}; ST_FPC=id=218d3f36f1e70a627191547027958397:lv=1547027958397:ss=1547027958397:lsv=1547027958397:vs=1:spv=1",
    'Host': "search.secoo.com",
    'Referer': "http://search.secoo.com/search?keyword=ideage&firstcategoryid=0&secondcategoryid=0&thirdcategoryid=0&brandId=6717&level=0&orderType=4&filterType=0&source=&pageNo=1&st=10&price=0&prop=0&warehouse=100&actscr=0&expKey=",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "fa1af83f-ee16-4fd6-b941-d29a0f35b170"
    }
#
# querystring = {
#     "keyword":"ideage",
#     "firstcategoryid":"0",
#     "secondcategoryid":"0",
#     "thirdcategoryid":"0",
#     "brandId":"0",
#     "level":"0",
#     "orderType":"4",
#     "filterType":"0",
#     "source":"",
#     "pageNo":"3",
#     "st":"10",
#     "price":"0",
#     "prop":"0",
#     "warehouse":"100",
#     "actscr":"0",
#     "expKey":""}
for i in range(1, 4):
    page = str(i)
    querystring = {"keyword":"ideage","firstcategoryid":"0","secondcategoryid":"0","thirdcategoryid":"0","brandId":"0","level":"0","orderType":"4","filterType":"0","source":"","pageNo":page,"st":"10","price":"0","prop":"0","warehouse":"100","actscr":"0","expKey":""}
    one_page = requests.get(ideage_url, querystring, headers=home_headers)
    print(one_page)
    soup = BeautifulSoup(one_page.text, 'lxml')
    one_page_items = soup.select('body > div.product_box > div.commodity-list.clearfix > dl')
    one_page_lst = []
    for one_item in one_page_items:
        itemid = one_item.attrs['dlproid']
        title = one_item.select('dt > a')[0].attrs['title']
        if one_item.select('div > dd.mini_nav'):
            sell30 = one_item.select('div > dd.mini_nav > div > ul.clearfix > li')[0].attrs['sell30']
        else:
            sell30 = 0
        one_page_lst.append((itemid, title, sell30))
    df = pd.DataFrame(one_page_lst)
    df.to_csv('d:\\test\\siku_count.csv', mode='a+')

