import sys
from ctypes import *

def get_encrypt_value(data):
    if sys.platform == "win32":
        cur = cdll.LoadLibrary("movie_spa2/bestV8_win64.dll")
    else:
        raise Exception("unknown systerm!")

    result = bytes(20000)
    cur.runJs.argtypes = (c_char_p, c_char_p)
    for x in range(1):
        cur.runJs(create_string_buffer(data.encode('utf8')), result)
        # print(result.rstrip(b"\x00"))

data = open("movie_spa2/export_module.js","r").read()

get_encrypt_value(data)

