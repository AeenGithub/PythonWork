# -*- coding: utf-8 -*-
"""
Created on Thu May 17 19:28:42 2018

@author: S103878
"""

import json

import requests

s = requests.Session()
f_url = r'http://scm.semir.cn/DIM-Demo/zmsmg/supplierMgr/getSupplierInfoList'
f_data = {'search_EQ_lifnr': '',
          'search_EQ_suppliername': '001100001',
          'search_EQ_hzzt': '',
          'search_EQ_amb': '', 
          'search_EQ_funcTyp': '1',
          'page': '1',
          'rows': '15'
          }
header = {'Host': 'scm.semir.cn',
          'Connection': 'keep-alive',
          'Content-Length': '114',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Origin': 'http://scm.semir.cn',
          'X-Requested-With': 'XMLHttpRequest',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          }
a = s.request('post', f_url, params=f_data)
pa = json.loads(a.text)['rows'][0]['licenseregistereddate']
dfg = str({"licenseregistereddate":pa, "franchisebrand":"1000"})
s_data = {'hearScorecardInfo': dfg}
b = s.request('post', r'http://scm.semir.cn/DIM-Demo/zmsmg/supplierAnonymityRegister/getSmgAnonymityregister', params=s_data)
print(json.loads(b.text))



