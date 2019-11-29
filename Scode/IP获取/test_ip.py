# -*- coding: utf-8 -*-
"""
Created on Thu May 31 08:26:53 2018

@author: S103878
"""


import requests
#import random 
#import time
#from requests.exceptions import Timeout
with open('d:\\HTTPS.txt', 'r', encoding='utf-8') as f:
    file = f.read()
    lst_file = file.strip(' ').split('\n')
    
lst_headers = [  
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},  
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6', 'Connection': 'close'},  
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},  
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},  
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},  
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ] 


for proxy in lst_file:
    print(proxy)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
        }
#        headers = random.choice(lst_headers)
    headers = lst_headers[1]
    requests.adapters.DEFAULT_RETRIES = 5
    try:
#        time.sleep(5)
#            s = requests.Session()
#            s.keep_alive = False
        res = requests.get(r'http://2018.ip138.com/ic.asp', headers=headers, proxies=proxies, timeout=1)
        print(res.status_code)
        if res.status_code == 200:
            with open('d:\\ips.txt', 'w', encoding='utf-8') as ipg:
                ipg.write(proxy)
                ipg.write('\n')       
    except Exception as e:
        print('HttpError')
        continue