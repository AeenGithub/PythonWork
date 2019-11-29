# -*- coding: utf-8 -*-
"""
Created on Thu May 31 20:53:49 2018

@author: S103878
"""

import random
import time

import requests


class Spider_Ips():  
    url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=9c9c619aa27a4efe8b7185bb05374172&orderno=YZ20185313785q5fsOl&returnType=1&count=10'  
    headers = [  
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},  
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},  
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},  
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},  
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},  
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}  
    ]  
    MAX_RETRIES = 20  
    session = requests.Session()  
    adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)  
    session.mount('https://', adapter)  
    session.mount('http://', adapter)  
    
    
    def list_ip(self):
        for i in range(100):
            print(i)
            time.sleep(5.5)
            req = self.session.get(self.url, headers=random.choice(self.headers))  
            with open('d:\\HTTPS.txt', 'a', encoding='utf-8') as f:  
                print(req.text)  
                f.write(req.text+'\n')                      
  
    
    def __init__(self):  
        self.list_ip()  
  
  
s_ip = Spider_Ips()  