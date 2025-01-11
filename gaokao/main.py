import sys
from ctypes import *

def get_encrypt_value(data):
    if sys.platform == "win32":
        cur = cdll.LoadLibrary("gaokao/bestV8_win64.dll")
    else:
        raise Exception("unknown systerm!")

    result = bytes(20000)
    cur.runJs.argtypes = (c_char_p, c_char_p)
    for x in range(1):
        cur.runJs(create_string_buffer(data.encode('utf8')), result)
        # print(result.rstrip(b"\x00"))
        aa = result.rstrip(b"\x00").decode('utf-8')
        return aa

page = 145
init_url = "https://api.eol.cn/web/api/?keyword=&page={}&province_id=&ranktype=&request_type=1&size=20&top_school_id=1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375&type=&uri=apidata/api/gkv3/school/lists".format(page)
one = '''{}"{}"'''.format('j = ', init_url)
two = '''t = {"SIGN": "D23ABC@#56", str: j.replace(/^\/|https?:\/\/\/?/, "")}'''
three = '''result = chook(360)(v(t))\nresult'''

new_part = '{}\n{}\n{}'.format(one, two, three)

with open("gaokao/webspack_gaokao.js","r") as f:
    js_code = f.read()
    js_code = js_code + '\n' + new_part

# print(js_code)
signsafe = get_encrypt_value(js_code)
last_url = '''{}&signsafe={}'''.format(init_url, signsafe)
print(last_url)


