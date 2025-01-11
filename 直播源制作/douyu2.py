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
    
def get_comple_js(t):
    one = ""
    two = """""".format(t)
    three = """"""

    new_part = ""
    new_part = "{}\n{}\n{}".format(one, two, three)

    with open("直播源制作/js/url_product.js", "r") as f:
        js_code = f.read()
        js_code = js_code + "\n" + new_part
        # print(js_code)
    return js_code

t = ''
js_code = get_comple_js(t)
print(js_code) 

sign = get_encrypt_value(js_code)