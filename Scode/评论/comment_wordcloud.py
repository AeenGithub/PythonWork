# coding:utf-8
import csv

import pynlpir

lst_key_words = []
with open(r"E:\文档\爬虫\潮牌TOP评论需求_结果.xlsx", 'r', encoding='gbk') as f:
	csv_reader = csv.DictReader(f)
	for row in csv_reader:
		pass
pynlpir.open(encoding='utf-8')

s = r'''不满意，老公穿了一天身上都是黑色的毛毛，说我这次买的衣服质量太差，
放在盆里洗，换三次水还是好多毛毛，估计穿不了几次衣服就不成样子了，不联系购买，
白色的估计也掉毛毛，只是白色不明显罢了。
'''
key_words = pynlpir.get_key_words(s)
seg = pynlpir.segment(s)
print(key_words)
# print(seg)