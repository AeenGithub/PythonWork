import time

import requests
from requests_toolbelt import MultipartEncoder


class Douban(object):

	def __init__(self):
		self.init_url = 'https://www.douban.com/'
		self.risk_url = 'https://login.xunlei.com/risk?cmd=report'
		self.login_url = 'https://login.xunlei.com/xluser.core.login/v3/login'
		self.home_url = 'https://i.xunlei.com/xluser/home.html'
		self.timestamp = str(int(time.time()*1000))
		self.headers = {
		'Host': 'login.xunlei.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://i.xunlei.com/login/?r_d=1&use_cdn=0&timestamp={}&refurl=https%3A%2F%2Fi.xunlei.com%2Fxluser%2Flogin.html'.format(self.timestamp),
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': '549',
		'Cookie': 'appidstack=22003; _x_t_=0',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1'
		}

	def start_requests(self):
		post_data = {
			'cachetime': self.timestamp,
			'xl_fp':'01bda6b3ae926069bf69e353bc69161c',
			'xl_fp_raw':'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXaW42NDsgeDY0OyBydjo2MS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzYxLjAjIyN6aC1DTiMjIzI0IyMjOTAweDE2MDAjIyMtNDgwIyMjdHJ1ZSMjI3RydWUjIyN0cnVlIyMjdW5kZWZpbmVkIyMjdW5kZWZpbmVkIyMjIyMjV2luNjQjIyN1bnNwZWNpZmllZCMjI1Nob2Nrd2F2ZSBGbGFzaDo6U2hvY2t3YXZlIEZsYXNoIDI5LjAgcjA6OmFwcGxpY2F0aW9uL3gtc2hvY2t3YXZlLWZsYXNofnN3ZixhcHBsaWNhdGlvbi9mdXR1cmVzcGxhc2h+c3BsIyMjYzdmZTUzMmE4MjhkNGRkMTNjMzcyMmQwOTJhMjcxNjA=',
			'xl_fp_sign': '74ab0437e11c7a5e722383af11a9bf29'
		}
		mutli_data = MultipartEncoder(
			fields={
			'field0': 'value', 
			'field1': 'value',
			"appid": '22003',
			"appName": 'WEB-i.xunlei.com',
			"deviceModel": 'Firefox: 61.0',
			"deviceName": 'FF',
			"OSVersion": 'Win64',
			"provideNname": 'NONE',
			"netWorkType": 'NONE',
			"providerName": 'NONE',
			"sdkVersion": 'v3.2.1',
			"clientVersion": '1.1.1',
			"protocolVersion": '301',
			"devicesign": 'wdi10.0793a98a61a61ee8afaeedd7aed52dcf07b2ab919b27e4243c4bb7c11903ecab',
			"platformVersion": '1',
			"fromPlatformVersion": '1',
			"format": 'cookie',
			"timestamp": self.timestamp,
			"userName": '2500754801@qq.com',
			"passWord": '..dtz..384',
			"isMd5Pwd": '0',
			"creditkey": ''
			}
		)
		add_headers = self.headers
		add_headers['Content-Type'] = mutli_data.content_type
		with requests.Session() as s:
			first_post = s.post(self.risk_url, data=post_data, headers=self.headers)
			s.cookies.set('userName', '2500754801@qq.com')
			second_post = s.post(self.login_url, data=mutli_data, headers=self.headers)
			# home = s.get(self.home_url, headers=self.headers)
			# home.encoding = 'utf-8'
			print(first_post.status_code)
			print(first_post.headers)
			print(second_post.status_code)
			print(second_post.headers)
			# print(home.request.headers)
		return ''

if __name__ == '__main__':
	douban = Douban()
	douban.start_requests()

