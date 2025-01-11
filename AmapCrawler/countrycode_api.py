#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

import requests
import json
import pandas as pd

url = 'https://dmfw.mca.gov.cn/web/department/list.html'

response = requests.get(url, params={'year': '2019'})
json_data = json.loads(response.text)
df = pd.DataFrame(json_data)

print(df)

# df.to_excel('新版国家行政区划代码表.xlsx')