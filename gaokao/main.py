import sys
from ctypes import *

DLL_PATH = "gaokao/bestV8_win64.dll"
JS_FILE_PATH = "gaokao/webspack_gaokao.js"
PAGE = 145
INIT_URL_TEMPLATE = "https://api.eol.cn/web/api/?keyword=&page={}&province_id=&ranktype=&request_type=1&size=20&top_school_id=1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375&type=&uri=apidata/api/gkv3/school/lists"

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

def main():
    init_url = INIT_URL_TEMPLATE.format(PAGE)
    new_part = generate_js_code(init_url)

    try:
        with open(JS_FILE_PATH, "r") as f:
            js_code = f.read() + '\n' + new_part
    except FileNotFoundError:
        print(f"JavaScript file not found: {JS_FILE_PATH}")
        return

    signsafe = get_encrypt_value(js_code)
    if signsafe:
        last_url = f"{init_url}&signsafe={signsafe}"
        print(last_url)
    else:
        print("Failed to generate signsafe value.")

if __name__ == "__main__":
    main()


