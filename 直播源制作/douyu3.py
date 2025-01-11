import requests
import time

cookies = {
    'dy_did': 'a601d80e583453a01c12d67900051601',
    'acf_did': 'a601d80e583453a01c12d67900051601',
    'Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7': '1690559058,1690606997,1690624859,1690626417',
    'Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7': '1690626581',
}

headers = {
    'authority': 'www.douyu.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,ga;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    # 'content-length': '0',
    # 'cookie': 'dy_did=a601d80e583453a01c12d67900051601; acf_did=a601d80e583453a01c12d67900051601; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1690559058,1690606997,1690624859,1690626417; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1690626581',
    'origin': 'https://www.douyu.com',
    'pragma': 'no-cache',
    'referer': 'https://www.douyu.com/79213?dyshid=0-a601d80e583453a01c12d67900051601&dyshci=1',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

params = {
    'v': '220120230729',
    'did': 'a601d80e583453a01c12d67900051601',
    'tt': round(time.time()),
    'sign': '3c5a453bde8770d62ac79f5aab54c601',
    'cdn': '',
    'rate': '-1',
    'ver': 'Douyu_222082905',
    'iar': '1',
    'ive': '1',
    'hevc': '0',
    'fa': '0',
}

response = requests.post('https://www.douyu.com/lapi/live/getH5Play/79213', params=params, cookies=cookies, headers=headers)
print(response.json())