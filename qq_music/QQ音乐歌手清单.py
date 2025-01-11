import sys
from ctypes import *
import time
import json
import pandas as pd
import requests
import time

# 传入js文件，将js文件的结果返回
def get_encrypt_value(data):
    if sys.platform == "win32":
        cur = cdll.LoadLibrary("gaokao/bestV8_win64.dll")
    else:
        raise Exception("unknown systerm!")
    result = bytes(20000)
    cur.runJs.argtypes = (c_char_p, c_char_p)
    for x in range(1):
        cur.runJs(create_string_buffer(data.encode("utf8")), result)
        # print(result.rstrip(b"\x00"))
        uresult = result.rstrip(b"\x00").decode("utf-8")
        return uresult

# 从json中上获取
# total_singer = 7370
total_page = 93
init_url = "https//u.y.qq.com/cgi-bin/musics.fcg"

# data = '{"comm":{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"yqq.json","needNewCode":1,"uin":0,"g_tk_new_20200303":5381,"g_tk":5381},"req_1":{"module":"music.musichallSinger.SingerList","method":"GetSingerListIndex","param":{"area":-100,"sex":-100,"genre":-100,"index":-100,"sin":160,"cur_page":3}}}'
def get_post_data(cur_page):
    sin = 0 + 80 * cur_page
    dict_data = {
    "comm": {
        "cv": 4747474,
        "ct": 24,
        "format": "json",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "notice": 0,
        "platform": "yqq.json",
        "needNewCode": 1,
        "uin": 0,
        "g_tk_new_20200303": 5381,
        "g_tk": 5381,
    },
    "req_1": {
        "module": "music.musichallSinger.SingerList",
        "method": "GetSingerListIndex",
        "param": {
            "area": -100,
            "sex": -100,
            "genre": -100,
            "index": -100,
            "sin": sin,
            "cur_page": cur_page,
        },
    },
}
    data = (json.dumps(dict_data)).replace(' ', '')
    return data

def get_comple_js(t):
    one = ""
    two = """t={}""".format(t)
    three = """sign = o(t.data)\nsign\n"""

    new_part = ""
    new_part = "{}\n{}\n{}".format(one, two, three)

    with open("qq_music/main.js", "r") as f:
        js_code = f.read()
        js_code = js_code + "\n" + new_part
        # print(js_code)
    return js_code

cookies = {
    'pgv_pvid': '5212857804',
    'qq_domain_video_guid_verify': '1e40ac467d5cea0d',
    'eas_sid': '2166b898q1F361S8V343l1Y6j2',
    'ptui_loginuin': '2500754801',
    'RK': 'SEMtxZPJ5V',
    'ptcz': '6985dcfdd1a04ff0903bf9aa8f5ceb91bda8b635054174b4abd33ad45ade0948',
    'uin_cookie': 'o2500754801',
    'ied_qq': 'o2500754801',
    'LOLWebSet_AreaBindInfo_2500754801': '%257B%2522areaid%2522%253A%25228%2522%252C%2522areaname%2522%253A%2522%25E6%2588%2598%25E4%25BA%2589%25E5%25AD%25A6%25E9%2599%25A2%2520%25E7%2594%25B5%25E4%25BF%25A1%2522%252C%2522sRoleId%2522%253A0%252C%2522roleid%2522%253A%25222500754801%2522%252C%2522rolename%2522%253A%2522%25E5%258D%2583%25E5%258F%25B6%25E6%2580%259D%25E9%259B%25A8%2522%252C%2522checkparam%2522%253A%2522lol%257Cyes%257C2500754801%257C8%257C2500754801*%257C%257C%257C%257C%2525E5%25258D%252583%2525E5%25258F%2525B6%2525E6%252580%25259D%2525E9%25259B%2525A8*%257C%257C%257C1688132072%257C%2522%252C%2522md5str%2522%253A%252254A90C403F64FA2C759B76415B237E0E%2522%252C%2522roleareaid%2522%253A%25228%2522%252C%2522sPartition%2522%253A%25228%2522%257D',
    'o_cookie': '2500754801',
    'fqm_pvqid': '20983056-b5cb-4114-a7d5-8c2964ced598',
    'ts_uid': '3156433726',
    'fqm_sessionid': '3e364f7e-5467-4df4-9805-4b8e81405a13',
    'pgv_info': 'ssid=s2757541020',
    'ts_last': 'y.qq.com/n/ryqq/singer_list',
}

headers = {
    "authority": "u.y.qq.com",
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,ga;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://y.qq.com",
    "pragma": "no-cache",
    "referer": "https://y.qq.com/",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

cur_page = 1
for i_page in range(total_page):
    cur_page = i_page + 1
    print('第{}页开始下载'.format(cur_page))
    data = get_post_data(cur_page)
    t = {"type": "POST", "data": data}
    js_code = get_comple_js(t)
    sign = get_encrypt_value(js_code)
    time_stamp = round(time.time() * 1000)
    params = {"_": time_stamp, "sign": sign}
    response = requests.post(url="https://u.y.qq.com/cgi-bin/musics.fcg",
                             params=params,
                             cookies=cookies,
                             headers=headers,
                             data=data
    )
    res_text = response.text
    json_data = json.loads(res_text)
    singerlist = json_data['req_1']['data']['singerlist']
    df = pd.DataFrame(singerlist)
    df.to_csv('E:\\Python\\qq_music\\singerlist.csv', mode='a', index=False)
    print('第{}页下载完成\n'.format(cur_page))
    time.sleep(2)
