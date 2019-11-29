# -*- coding: utf-8 -*-
import copy
import json
from datetime import datetime

import scrapy
from XiaomiYoupin.items import XiaomiyoupinItem


class XimyoupinSpider(scrapy.Spider):
    name = 'XimYoupin'
    allowed_domains = ['mi.com']
    url = 'https://youpin.mi.com/app/shopv3/pipe'
    detail_url = 'https://www.xiaomiyoupin.com/api/gateway/detail'
    start_urls = ['https://youpin.mi.com/']

    def done_param(self,res_name, action, data_id):
        result = {"model": "Homepage"}
        result["action"] = action
        result["parameters"] = data_id
        data = {
            res_name: result
        }
        final = {
            'data': json.dumps(data)
        }
        return final
    
    def comment_param(self, gid):
        overView = {
            "model": "Product",
            "action": "CommentIndexV2",
            "parameters": {'gid': gid}
            }
        # 规定了评论的页数和评论的每页含量
        param = {"index_type": 0, "gid": gid, "pindex": 1, "psize": 10, "tag_name": None}
        type_lst = {
            "model": "Product",
            "action": "CommentListOnly",
            "parameters": param
            }
        data = {
            'overView': overView,
            'list': type_lst
            }
        final = {
            'data': json.dumps(data)
        }
        return final

    def start_requests(self):
        action = "GetGroup2ClassInfo"
        data_id = {}
        param_data = self.done_param("result", action, data_id)
        yield scrapy.FormRequest(
            url=self.url,
            formdata=param_data,
            dont_filter=True,
            callback=self.parse_home
            )

    def parse_home(self, response):
        action = 'BuildHome'
        json_data = json.loads(response.text)
        clss_groups = json_data['result']['result']['data']['groups']
        for one_groups in clss_groups[1:-1]:
            for agroup in one_groups:
                item = XiaomiyoupinItem()
                if str(agroup['class']['ucid']) == '93':
                    item['senior_class'] = agroup['class']['name']
                    item['senior_id'] = agroup['class']['ucid']
                    one_item_id = {
                        "id": str(agroup['class']['ucid'])
                    }
                    param_data = self.done_param(res_name="uClassList", action=action, data_id=one_item_id)
                    yield scrapy.FormRequest(
                        url=self.url,
                        formdata=param_data,
                        dont_filter=True,
                        callback=self.parse_detail,
                        meta={'item': copy.deepcopy(item)}
                        )

    def parse_detail(self, response):
        item = response.meta['item']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text)
        clss_groups = json_data['result']['uClassList']['data']
        for one_content in clss_groups[1:]:
            if one_content.get('content'):
                content = one_content['content']['name']
                for one_product in one_content['data']:
                    if one_product['gid'] > 1000:
                        item['content'] = content
                        if one_product.get('ctime'):
                            item['create_time'] = datetime.strftime(datetime.fromtimestamp(one_product.get('ctime')), "%Y-%m-%d")
                        else:
                            item['create_time'] = '00-00-00'
                        if one_product.get('end'):
                            item['end_time'] = datetime.strftime(datetime.fromtimestamp(one_product.get('end')), "%Y-%m-%d")
                        else:
                            item['end_time'] = '00-00-00'
                        item['product_name'] = one_product['name']
                        item['gid'] = one_product['gid']
                        one_id= copy.deepcopy(one_product['gid'])
                        item['market_price'] = one_product['market_price']/100
                        item['order_overdue'] = one_product['order_overdue']
                        item['price_min'] = one_product['price_min']/100
                        item['sale_mode'] = one_product['sale_mode']
                        item['sale_count'] = one_product['saled']
                        item['sale_fee'] = one_product['saled_fee']
                        item['summary'] = one_product['summary']
                        item['url'] = one_product['url']
                        item['Img800'] = one_product['Img800']
                        if one_product.get('start'):
                            utime = datetime.fromtimestamp(int(one_product['start']))
                            item['start_time'] = utime.strftime('%Y-%m-%d')
                        else:
                            item['start_time'] = '00-00-00'
                        # print(one_id)
                        # print(item)
                        yield scrapy.FormRequest(
                            url=self.url,
                            formdata=self.comment_param(one_id),
                            dont_filter=True,
                            callback=self.parse_comment,
                            meta={'item': copy.deepcopy(item)}
                            )


    def parse_comment(self, response):
        item = response.meta['item']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text)
        # positive_rate = json_data['result']['overView']['data']['positive_rate']
        tags = json_data['result']['overView']['data']['tags']
        # print(item['gid'])
        # print(parse.unquote(response.request.body.decode('utf-8')))
        tag_lst = []
        for one_tag in tags:
            if one_tag['name'] != '全部' and one_tag['name'] != '有图':
                tag_lst.append(one_tag['name']+'|'+str(one_tag['count']))
            else:
                tag_lst.append('')
        comment_tag = '\t'.join(tag_lst)
        item['comment_tag'] = comment_tag
        item_url = copy.deepcopy(item['url'])
        item_god = copy.deepcopy(item['gid'])
        groupParams = [[item_god]]
        detail_data = {"groupName": "details",
                       "groupParams": groupParams,
                       "methods": [],
                       "version": "1.0.0",
                       "debug": False,
                       "channel": ""}
        detail_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
            'Referer': item_url,
            'Content-Type':'application/json'
        }
        dumps_detail_data = json.dumps(detail_data)
        yield scrapy.Request(
            url =  self.detail_url,
            method='POST',
            headers = detail_headers,
            body = dumps_detail_data,
            dont_filter = True,
            meta={'item': copy.deepcopy(item)},
            callback=self.size_detail
        )

    def size_detail(self, response):
        '''对单款数据进行抓取，获取单款数据到尺码的销售信息'''
        item = response.meta['item']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text)
        productInfo = json_data['data']['goods']['productInfo']
        for keys, one_size in productInfo.items():
            one_size_pid = one_size['pid']
            one_size_saled = one_size['saled']
            one_size_inventory = one_size['inventory']
            one_size_name = one_size['name']
            item['one_size_pid'] = one_size_pid
            item['one_size_saled'] = one_size_saled
            item['one_size_inventory'] = one_size_inventory
            item['one_size_name'] = one_size_name
            yield item
