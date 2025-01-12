import sys
from ctypes import *
import requests
import sqlite3 as sql3
import pandas as pd

DLL_PATH = "gaokao/bestV8_win64.dll"
JS_FILE_PATH = "gaokao/webspack_gaokao.js"
PAGE = 1
INIT_URL_TEMPLATE = "https://api.eol.cn/web/api/?keyword=&page={}&province_id=&ranktype=&request_type=1&size=20&top_school_id=[1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375]&type=&uri=apidata/api/gkv3/school/lists"
DATA_PATH = r"D:\SQLBASE\sdata.db"

HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.gaokao.cn',
    'priority': 'u=1, i',
    'referer': 'https://www.gaokao.cn/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
}

def get_encrypt_value(data):
    if sys.platform != "win32":
        raise Exception("unknown system!")

    try:
        cur = cdll.LoadLibrary(DLL_PATH)
        result = bytes(20000)
        cur.runJs.argtypes = (c_char_p, c_char_p)
        cur.runJs(create_string_buffer(data.encode('utf8')), result)
        return result.rstrip(b"\x00").decode('utf-8')
    except Exception as e:
        print(f"Error loading DLL or running JS: {e}")
        return None

def generate_js_code(init_url):
    one = '''{}"{}"'''.format('j = ', init_url)
    two = '''t = {"SIGN": "D23ABC@#56", str: j.replace(/^\/|https?:\/\/\/?/, "")}'''
    three = '''result = chook(360)(v(t))\nresult'''
    return '{}\n{}\n{}'.format(one, two, three)

def gen_signsafe(PAGE=1):
    init_url = INIT_URL_TEMPLATE.format(PAGE)
    new_part = generate_js_code(init_url)
    try:
        with open(JS_FILE_PATH, "r") as f:
            js_code = f.read() + '\n' + new_part
    except FileNotFoundError:
        print(f"JavaScript file not found: {JS_FILE_PATH}")
        return None
    return get_encrypt_value(js_code)

def get_page_json(PAGE=1):
    print(f"Getting page {PAGE}...")
    signsafe = gen_signsafe(PAGE)
    if not signsafe:
        return None, 0
    json_data = {
        'keyword': '',
        'page': PAGE,
        'province_id': '',
        'ranktype': '',
        'request_type': 1,
        'signsafe': signsafe,
        'size': 20,
        'top_school_id': '[1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375]',
        'type': '',
        'uri': 'apidata/api/gkv3/school/lists',
    }
    last_url = INIT_URL_TEMPLATE.format(PAGE) + "&signsafe=" + signsafe
    response = requests.post(headers=HEADERS, url=last_url, json=json_data)
    res_json = response.json()
    if res_json.get("code") == 403:
        print("403 Forbidden")
        return None, 0
    res_lst = res_json.get("data").get("item")
    res_num_found = res_json.get("data").get("numFound")
    print(f"Got page {PAGE}")
    return res_lst, res_num_found

def save_to_db(data, conn):
    df = pd.DataFrame(data)
    df.to_sql("college", conn, if_exists="append", index=True)

def loop_get_json():
    with sql3.connect(DATA_PATH) as conn:
        res_lst_first, res_num_found = get_page_json(PAGE)
        if res_lst_first:
            save_to_db(res_lst_first, conn)
        total_page = res_num_found // 20 + 1
        for i in range(2, total_page + 1):
            page_res_lst, _ = get_page_json(i)
            if page_res_lst:
                save_to_db(page_res_lst, conn)
                print(f"Page {i} done.")
        print("All pages done.")

if __name__ == "__main__":
    loop_get_json()


