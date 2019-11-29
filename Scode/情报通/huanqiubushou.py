# coding: utf-8

import json
import re
import time

import pandas as pd
import requests

url_home = r'http://m.51bushou.com'
url_purpose = r'https://m.51bushou.com/ygg-hqbs/cms/detail1?cId=112&APPOS=1&caid=389&gpm=0-48'
home_info = r'https://m.51bushou.com/ygg-hqbs/homePage/homeInfo30'
second_page = r'https://m.51bushou.com/ygg-hqbs/cms/detail1?cId=112&APPOS=1&caid=389&gpm=0-48'


headers = {
	'authority': 'm.51bushou.com',
	'path': '/ygg-hqbs/cms/detail1?cId=112&APPOS=1&caid=389&gpm=0-48',
	'Accept-Encoding': 'br, gzip, deflate',
	'Connection': 'keep-alive',
	'Accept': 'application/json',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A5345f/ios/globalscanner/3.6',
	'Accept-Language': 'zh-cn',
	'X-Requested-With': 'XMLHttpRequest'
	}


def get_first_page():
	first_page_navition = []
	with requests.Session() as s:
		s.get(url_home, headers=headers)
		# s.get(url_purpose)
		first_page = s.post(home_info, headers=headers)
		navigationBarList = json.loads(first_page.text)['navigationBarList']
		for one_navigation in navigationBarList:
			# print(type(one_navigation))
			one_navigation_detail = one_navigation['url']
			first_page_navition.append([one_navigation['name'], one_navigation_detail])
			first_page_navition = [[i[0], i[1].replace('index.html', 'detail1')] for i in first_page_navition if i[1] is not None]
		# print(first_page_navition)
	return first_page_navition

def get_second_page(url):
	final_url = []
	# url = r'https://m.51bushou.com/ygg-hqbs/cms/detail1?cId=1195&APPOS=1&caid=1170&gpm=0-48'
	second_page = requests.get(url, headers=headers).text
	pagetitle = json.loads(second_page)['pageTitle']
	all_url = re.findall(r'"url":"(.*?)","width"', second_page)
	need_url = [i for i in all_url if 10 < len(i) < 50]
	for i in need_url:
		if 'cnty' in i:
			url = i[12:]
		else:
			url = r'https://m.51bushou.com/ygg-hqbs/cms/detail1?' + i[16:]
		final_url.append(url)
	final_url = [i for i in final_url if i.isdigit() or 'APPOS' in i]
	return final_url

def get_third_page_two(num):
	url_toacsp = r'https://m.51bushou.com/ygg-hqbs/cnty/toacsp'
	url_detail = r'https://m.51bushou.com/ygg-hqbs/cnty/toac/detail?productIdList='
	data_toacsp = {'commonActivityId': num}
	with requests.Session() as s:
		s.get(url_home, headers=headers)
		toacsp = s.post(url_toacsp, headers=headers, data=data_toacsp).text
		wxShareTitle =  json.loads(toacsp)['wxShareTitle']
		lst = json.loads(toacsp)['productIdList'].split(',')
		change_lst = []
		change_lst = [','.join(lst[i:i+20]) for i in range(0, len(lst), 20)]
		all_lst_detail = []
		for one_detail in change_lst:
			detail_url = url_detail + one_detail
			detail_lst = requests.get(detail_url, headers=headers).text
			productDetailList = json.loads(detail_lst)['productDetailList']
			for one_item in productDetailList:
				all_lst_detail.append(one_item['name'])
		# return productDetailList
		return {wxShareTitle: all_lst_detail}
# url = r'https://m.51bushou.com/ygg-hqbs/cms/detail1?cId=1786&APPOS=1'
def get_third_page_one(url):
	all_class_dict = {}
	second_class_name = []
	with requests.Session() as s:
		s.get(url_home, headers=headers)
		s.get(url_purpose)
		bushou_res = requests.get(url, headers=headers)
	# bushou_soup = BeautifulSoup(bushou_res.text, 'lxml')
	# bushou_id = bushou_soup.select('#cms-24132')
	bushou_json = json.loads(bushou_res.text)
	pageTitle = bushou_json['pageTitle']
	try:
		second_class =  bushou_json['componentList'][1]
		second_cmsList = second_class['cmsList']
	except IndexError:
		second_cmsList = []
	for one in second_cmsList:
		try:
			# print(one['navigationName'])
			second_class_name.append(one['navigationName'])
		except KeyError as e:
			pass
	if second_class_name is True:
		other = bushou_json['componentList'][2:]
		for index, one_class in enumerate(other):
			one_class_lst = []
			one_class_name = second_class_name[index]
			for one in one_class['cmsList']:
				one_class_lst.append(one['name'])
			all_class_dict[one_class_name] = one_class_lst
		return {pageTitle: all_class_dict}
	else:
		all_name = re.findall(r'"name":"(.*?)","status"', bushou_res.text)
		# print(all_name)
		return {pageTitle: all_name}
# print(get_first_page())
# print(get_second_page())
# print(get_third_page_one(url))

last_all_title = []
for fir_title, fir_url in get_first_page():
	print(fir_title)
	time.sleep(3)
	get_second_page = get_second_page(fir_url)
	if get_second_page is False:
		second_page_content = get_third_page_one(fir_url)
	else:
		one_title = []
		for sec_url in get_second_page:
			if sec_url.isdigit():
				# print(sec_url)
				time.sleep(3)
				one_last_navition = get_third_page_two(sec_url)
			else:
				# print(sec_url)
				time.sleep(3)
				one_last_navition = get_third_page_one(sec_url)
			print(one_last_navition.keys())
			one_title.append(one_last_navition)
		df = pd.DataFrame(one_title)
		df['名字'] = fir_title
	last_all_title.append(df)
print(len(last_all_title))

