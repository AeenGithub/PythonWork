# -*- coding: utf-8 -*-
import copy
import json
from datetime import datetime
from hashlib import md5

import scrapy
# from urllib import parse
from YitiaoCrawler.items import YitiaocrawlerItem


class YitiaoSpider(scrapy.Spider):
    name = 'Yitiao'
    allowed_domains = ['h5.yit.com']
    start_urls = ['https://h5.yit.com/activity/3699.html']
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Host': 'h5.yit.com',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://h5.yit.com/activity/3699.html',
        'Connection': 'keep-alive',
        'TE': 'Trailers'
    }

    def SideList(self, **kwargs):
        before_md5_lst = []
        xyz = 'yitshenghuoguan.xyz!'
        mt = 'fcategorynewclient.getFCategoryNewClient'
        timestamp = str(int(datetime.now().timestamp()*1000))
        firstdata = {
            '_aid': '1',
            '_dlv': 'NORMAL_USER',
            '_mt': mt,
            '_sm': 'md5',
            '_ts': timestamp,
            'security_type': 'None'
        }
        firstdata.update(kwargs)
        firstdata = dict(sorted(firstdata.items(), key=lambda item: item[0]))
        for one_param in firstdata.items():
            a, b = one_param
            before_md5_lst.append(a+'='+b)
        before_md5_str = ''.join(before_md5_lst)+xyz
        before_md5_xyz = before_md5_str.encode(encoding='UTF-8')
        firstdata['_sig'] = md5(before_md5_xyz).hexdigest()
        sorted_firstdata = dict(
            sorted(firstdata.items(), key=lambda item: item[0]))
        return sorted_firstdata

    def start_requests(self):
        # first_data = self.SideList()
        yield scrapy.FormRequest(
            url='https://h5.yit.com/apigw/m.api',
            formdata=self.SideList(),
            headers=self.headers,
            dont_filter=True,
            callback=self.parse_list
        )

    def parse_list(self, response):
        # print(parse.unquote(response.request.body.decode('utf-8')))
        json_data = json.loads(response.text)
        content = json_data['content'][0]['value'][0]['children']
        # 一条的热门专区到健康的大的分类
        for one_category in content[1:]:
            # 根据大的分类，循环，获取每一条ID和链接, 如：家居
            one_category_title = one_category['title']
            one_category_id = one_category['id']
            one_category_bannerList = 'https://h5.yit.com/' + one_category['bannerList'][0]['bannerLinkUrlH5']
            # print(one_category['title'], one_category['id'])
            # print(one_category['bannerList'][0]['bannerLinkUrlH5'])
            # 大类下的中间分类，如：床上用品
            for one_senior_children in one_category['children']:
                seconde_id = one_senior_children['id']
                # 床上用品， 居家布艺， 水杯水壶
                seconde_title = one_senior_children['title']
                # print(one_category_title, seconde_title)
                for third_category in one_senior_children['children']:
                    # print(third_category['id'])
                    third_category_id = third_category['id']
                    # 被子、枕头、四件套、床垫
                    for one_search in third_category['searchList']:
                        item = YitiaocrawlerItem()
                        searchId = one_search['searchId']
                        # 获取小类，如被子
                        searchTitle = one_search['searchTitle']
                        item['one_category_title'] = one_category_title
                        item['one_category_id'] = one_category_id
                        item['one_category_bannerList'] = one_category_bannerList
                        item['seconde_id'] = seconde_id
                        item['seconde_title'] = seconde_title
                        item['third_category_id'] = third_category_id
                        item['searchTitle'] = searchTitle
                        item['searchId'] = searchId
                        # 针对每一个search ID 获取下面的上平总数
                        new_data = {
                            'pageParameter': '{"offset":0,"limit":20}',
                            '_mt': 'search.searchForFCategoryV2',
                            'searchId': str(one_search['searchId'])
                        }
                        yield scrapy.FormRequest(
                            url='https://h5.yit.com/apigw/m.api',
                            formdata=self.SideList(**new_data),
                            headers=self.headers,
                            dont_filter=True,
                            callback=self.parse_category,
                            meta={'item': copy.deepcopy(item)}
                        )

    def parse_category(self, response):
        json_data = json.loads(response.text)['content'][0]
        # 获取每一个小类的总的宝贝数， 被子总数224
        all_page = int(json_data['totalCount'])//20+1
        for one_page in range(all_page):
            item = response.meta['item']
            item['totalCount'] = json_data['totalCount']
            search_id = item['searchId']
            item['page_seq'] = one_page+1
            offset = str(20 * one_page)
            pageparam = '{"offset":' + offset + ',"limit":20}'
            new_data = {
                'pageParameter': pageparam,
                '_mt': 'search.searchForFCategoryV2',
                'searchId': str(search_id)
            }
            # yield item
            yield scrapy.FormRequest(
                url='https://h5.yit.com/apigw/m.api',
                formdata=self.SideList(**new_data),
                headers=self.headers,
                dont_filter=True,
                callback=self.parse_morelst,
                meta={'item': copy.deepcopy(item)}
            )

    def parse_morelst(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text)['content'][0]
        for one_item in json_data['result']:
            item = response.meta['item']
            item['link_Url'] = one_item['linkUrl']
            item['categoryLevel3Name'] = one_item['categoryLevel3Name']
            item['categoryLevel2Name'] = one_item['categoryLevel2Name']
            item['mainImageUrl'] = one_item['mainImageUrl']
            item['productName'] = one_item['productName']
            item['supplierName'] = one_item['supplierName']
            item['productId'] = one_item['productId']
            item['secondTitle'] = one_item['secondTitle']
            item['title'] = one_item['title']
            item['stock'] = one_item['saleInfo']['stock']
            item['price'] = one_item['saleInfo']['priceInfo']['maxPriceInfo']['price']
            item['tagPrice'] = one_item['saleInfo']['priceInfo']['maxPriceInfo']['tagPrice']
            item['vip_Price'] = one_item['saleInfo']['priceInfo']['maxPriceInfo']['vipPrice']
            yield item


# if __name__ == '__main__':
#     yit = YitiaoSpider()
#     print(yit.SideList())
