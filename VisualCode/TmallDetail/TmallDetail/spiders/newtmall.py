# -*- coding: utf-8 -*-
import collections
import copy
import json
from datetime import datetime

import scrapy
from TmallDetail.items import TmalldetailItem


class NewtmallSpider(scrapy.Spider):
    name = 'newtmall'
    allowed_domains = ['tmall.com']
    start_urls = ['http://tmall.com/']
    filepath = "./config/name_itemid"

    def start_requests(self):
        shopname_url = collections.defaultdict()
        with open(self.filepath, encoding='utf-8') as f:
            for row in f.readlines():
                # 根据item_id建立item_id和品牌的对应关系字典
                shopname_url[row.split('\t')[1]] = row.split('\t')[0]
        for itemid in shopname_url:
            simple_headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(itemid)
            }
            brand_name = shopname_url[itemid]
            datenum = int((datetime.now() - datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds() * 1000)
            yield scrapy.Request(
                url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=8da5c2b4f4ddb2189c685a74c5d2a42c&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%7B%22itemNumId%22%3A%22{1}%22%7D'.format(
        datenum, itemid),
        #         url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={0}&sign=6298b3c5128b9220debf6963eb1d7873&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%22itemNumId%22%3A%22{1}%22'.format(
        # datenum, itemid),
                callback=self.parse,
                headers=simple_headers,
                dont_filter=True,
                meta={'itemid':copy.deepcopy(itemid),
                      'brand_name': copy.deepcopy(brand_name)},
                # errback=self.dealerror,
            )
    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        itemid = response.meta['itemid']
        brand_name = response.meta['brand_name']
        title = []
        contents = []
        try:
            json_data = json.loads(response.text[11:-1])
            try:
                basic_info = json_data['data']['props']['groupProps'][0]['基本信息']   #列表包含字典
                basic_info.insert(0, {'item_id': itemid})
                for one_title in basic_info:
                    title.extend(list(one_title.keys()))
                    contents.extend(list(one_title.values()))
                basic_contents = dict(zip(title, contents))
            except KeyError as e:
                basic_contents = ''
            sell_counts = json.loads(json_data['data']['apiStack'][0]['value'])
            transmitPrice = sell_counts['price']['transmitPrice']['priceText']
            try:
                oprice = sell_counts['price']['extraPrices'][0]['priceText']
            except KeyError as e:
                oprice = ''
            try:
                sellCount = sell_counts['item']['sellCount']
            except KeyError:
                sellCount = ''
            try:
                sell_img = sell_counts['item']['videos'][0]['videoThumbnailURL']
            except Exception:
                sell_img = ''
            result_price = dict(zip(['transmitPrice', 'oprice', 'sellCount', 'sell_img'], [transmitPrice, oprice, sellCount, sell_img]))
            try:
                startTime = sell_counts['vertical']['jhs']['startTime']
                endTime = sell_counts['vertical']['jhs']['endTime']
                soldCount = sell_counts['vertical']['jhs']['soldCount']
            except KeyError:
                startTime = endTime = soldCount = ''
            result_time = dict(zip(['startTime', 'endTime', 'soldCount'], [startTime, endTime, soldCount]))
            item = TmalldetailItem()
            item['itemid'] = itemid
            item['brand_name'] = brand_name
            item['basic_contents'] = json.dumps(basic_contents)
            item['result_price'] = json.dumps(result_price)
            item['result_time'] = json.dumps(result_time)
        except:
            pass
