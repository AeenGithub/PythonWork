# -*- coding:utf-8 -*-
import json
import os
import sys
import time

import md5
import requests
from qiniu import put_file

IQFA_ACCESS_KEY = "Amsb0VBTxOJBlCAhcSmRxA4O8gPLde6MBHoC_UdM"
IQFA_SECRET_KEY = "Jl-F0fqFTSzzHWLRa4rTkxnuQw4mZNAPWXtSZ5Pz"

IQFA_PIC_DOMAIN = "pez2d8qzl.bkt.clouddn.com"
IQFA_IP_ADDRESS = "47.94.71.29"
IQFA_SUPPORT_PROTOCOL = "http://"
IQFA_REQUEST_PATH = "/api/image/token"
#IQFA_REQUEST_PATH = "/api/video/token"


def sign(secret_key, params=None):
    if params:
        params = sorted(params)
        sign_string = secret_key
        for i in params:
            key, value = i
            sign_string += str(key)
            sign_string += str(value)
        sign_string += secret_key

        hash_string = md5.new()
        hash_string.update(sign_string)
        return hash_string.hexdigest().upper()
    else:
        pass


def requestWithFileName(file_name):
    time_stamp = int(time.time())
    params = [
        ("ACCESS_KEY", IQFA_ACCESS_KEY),
        ("TIMESTAMP", time_stamp),
        ("file_name", file_name)
    ]
    sign_string = sign(IQFA_SECRET_KEY, params)
    data = {
        "ACCESS_KEY": IQFA_ACCESS_KEY,
        "SIGN_KEY": sign_string,
        "TIMESTAMP": time_stamp,
        "file_name": file_name
    }
    resp = requests.post(IQFA_SUPPORT_PROTOCOL +
                         IQFA_IP_ADDRESS + IQFA_REQUEST_PATH, data=data)
    return resp.text


if __name__ == '__main__':
    f = open('url_list.txt', 'w')
    for i in range(10):  # 10 attemps in default
        print('Creating image url instance {}.'.format(i))
        res = requestWithFileName("Scra_test" + str(i) + ".jpg")
        a = "Res: {}".format(res)
        token = (json.loads(res)['token'])
        path = (json.loads(res)['path'])

        # local file directory
        loaclfile = 'Raw_images/' + sys.argv[1]
        ret, info = put_file(token, path, loaclfile)

        if info.status_code == 200:
            a = "Success Upload Qiniu: {}".format(loaclfile)
            a = os.path.join('http://otl6ypoog.bkt.clouddn.com', path)
            f.write(a + ' ')
        else:
            print("Upload Qiniu Failure !")
    f.close()
