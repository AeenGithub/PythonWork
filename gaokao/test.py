import json
import urllib.parse

json_data = {
    'keyword': '',
    'page': 4,
    'province_id': '',
    'ranktype': '',
    'request_type': 1,
    'signsafe': '5cb1441aa55d5a4c443e06d005edbe3e',
    'size': 20,
    'top_school_id': '[2461,436,1169,1975,434,1356,1159,435,1008,457,1946,3374,3288]',
    'type': '',
    'uri': 'apidata/api/gkv3/school/lists',
}

url_encoded_str = urllib.parse.urlencode(json_data)

print(url_encoded_str)

'https://api.eol.cn/web/api/?keyword=&page=1&province_id=&ranktype=&request_type=1&size=20&top_school_id=[1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375]&type=&uri=apidata/api/gkv3/school/lists'

