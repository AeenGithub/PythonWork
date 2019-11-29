# -*- coding: utf-8 -*-
import copy
import json
import math
import re

import scrapy
from UniqloSpidering.items import UniqlospideringItem


class UniqloofficialSpider(scrapy.Spider):
    name = 'UniqloOfficial'
    allowed_domains = ['uniqlo.cn']
    start_urls = ['http://www.uniqlo.cn/']
    json_headers = {
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Connection': "keep-alive",
        'Content-Length': "315",
        'Content-Type': "application/json",
        'Host': "d.uniqlo.cn",
        'Origin': "https://www.uniqlo.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
    }

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        dict_age = {
            'women_lst': response.css('#u-main-nav-list > div.nav-women-list.clearfix > dl > div'),
            'men_lst': response.css('#u-main-nav-list > div.nav-men-list.clearfix > dl > div'),
            'kids_lst': response.css('#u-main-nav-list > div.nav-kids-list.clearfix > dl > div'),
            'baby_lst': response.css('#u-main-nav-list > div.nav-baby-list.clearfix > dl > div')
        }
        for one_age in dict_age:
            for one_attr in dict_age[one_age]:
                # 获取男女婴童四大类的整体分类规则
                # 获取分类规则的小类名称和对应链接
                for one_senior in one_attr.css('div.nav-list-part'): # 测试
                    # 获取分类规则的大类名称，新作&特惠
                    attr_selector = one_senior.css('dt::text')
                    if attr_selector:
                        attr_name = attr_selector[0].extract()
                    else:
                        attr_name = ""
                    one_attr_name = [i.extract() for i in one_senior.xpath('.//dd/a/text()')]
                    one_attr_name.insert(0, '每周上新')
                    one_attr_url = [i.extract() for i in one_senior.xpath('.//dd/a/@href')]
                    one_attr_dict = dict(zip(one_attr_name, one_attr_url))
                    for one_clss in one_attr_dict:
                        item = UniqlospideringItem()
                        item['ageclss'] = one_age
                        item['junior_name'] = attr_name
                        item['senior_name'] = one_clss
                        item['senior_name_url'] = one_attr_dict[one_clss]
                        url_key = copy.deepcopy(one_attr_dict[one_clss])
                        yield item
                        if '/c' in url_key:
                            CategoryCode = url_key.split('/')[-1][:-5]
                            self.json_headers['Referer'] = 'https://www.uniqlo.cn/c/{}.html'.format(CategoryCode)
                            yield scrapy.Request(
                                url='https://d.uniqlo.cn/hmall-sc-service/search/searchWithCategoryCodeAndConditions/zh_CN',
                                method='POST',
                                body='{"url":"/c/%s.html","pageInfo":{"page":1,"pageSize":24,"withSideBar":"Y"},"belongTo":"pc","rank":"overall","priceRange":{"low":0,"high":0},"color":[],"size":[],"season":[],"material":[],"sex":[],"identity":[],"insiteDescription":"","exist":[],"categoryCode":"%s","searchFlag":"false","description":""}' % (
                                    CategoryCode, CategoryCode),
                                meta={'item': copy.deepcopy(item)},
                                dont_filter=True,
                                headers=self.json_headers,
                                callback=self.parse_detail
                            )
                        else:
                            html_url = url_key.split('#')[0]
                            real_url = 'https://www.uniqlo.cn/data/pages/__archived{}.json'.format(html_url)
                            other_headers = {
                                'Referer': 'https://www.uniqlo.cn{}'.format(html_url),
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/71.0.3578.98 Safari/537.36 '
                            }
                            yield scrapy.Request(
                                url=real_url,
                                headers=other_headers,
                                meta={'item': copy.deepcopy(item)},
                                dont_filter=True,
                                callback=self.parse_json
                        )
    def parse_detail(self, response):
        item = response.meta['item']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        Code = item['senior_name_url'].split('/')[-1][:-5]
        if response.status == 200:
            json_data = json.loads(response.text)
            resp = json_data['resp']
            productSum = resp[2]['productSum']
            pageSize = resp[2]['pageSize']
            total_page = math.ceil(float(productSum)/pageSize)
            for page in range(1, total_page+1):
                CategoryCode = copy.deepcopy(Code)
                self.json_headers['Referer'] = 'https://www.uniqlo.cn/c/{}.html'.format(CategoryCode)
                yield scrapy.Request(
                    url='https://d.uniqlo.cn/hmall-sc-service/search/searchWithCategoryCodeAndConditions/zh_CN',
                    method='POST',
                    body='{"url":"/c/%s.html?page=%s","pageInfo":{"page":%s,"pageSize":24,"withSideBar":"Y"},"belongTo":"pc","rank":"overall","priceRange":{"low":0,"high":0},"color":[],"size":[],"season":[],"material":[],"sex":[],"identity":[],"insiteDescription":"","exist":[],"categoryCode":"%s","searchFlag":"false","description":""}' % (
                        CategoryCode, page, page, CategoryCode),
                    meta={'item': copy.deepcopy(item)},
                    dont_filter=True,
                    headers=self.json_headers,
                    callback=self.parse_merchandise
                )
        else:
            item['ClassPicUrl'] = ""
            item['productName'] = ""
            item['mainPic'] = ""
            item['price'] = ""
            item['productCode'] = ""
            item['label'] = ""
            yield item

    def parse_merchandise(self, response):
        item = response.meta['item']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text)
        MerchandiseLst = json_data['resp'][1]
        for onemer in MerchandiseLst:
            item['ClassPicUrl'] = ""
            item['productName'] = onemer['productName']
            item['mainPic'] = onemer['mainPic']
            item['price'] = onemer['minPrice']
            item['productCode'] = onemer['productCode']
            item['label'] = onemer['label']
            yield item

    def parse_json(self, response):
        item = response.meta['item']
        # if item['senior_name_url'] == '/women_uld.html':
        #     raise ValueError
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        if response.status == 200:
            json_data = json.loads(response.text)
            json_lst = list(json_data.items())
            # selection 多余实际需求，通过下面的循环判断具有ProductGroup的selection和对应的前一个selection
            need_dict_keys = {}
            for index, one_selection in enumerate(json_lst):
                selection_value = one_selection[1]['component']
                if selection_value == 'ProductGroup':
                    need_dict_keys[json_lst[index - 1][0]] = one_selection[0]
            # 对挑选后的selection建立映射，然后循环取出对应数据，再进行解析
            if need_dict_keys:
                for one_key in need_dict_keys:
                    html = json_data[one_key].get('props').get('html')
                    picture_url = re.findall('src="(.*?.jpg)', html)[0]
                    for one_item in json_data[need_dict_keys[one_key]].get('props').get('items'):
                        item['ClassPicUrl'] = picture_url
                        item['productCode'] = one_item['productCode']
                        item['price'] = one_item['price']
                        item['mainPic'] = one_item['mainPic']
                        item['label'] = one_item['label']
                        item['productName'] = one_item['productName']
                        yield item
            else:
                item['ClassPicUrl'] = item['productCode'] = item['price'] = item['mainPic'] = item['label'] = item['productName'] = 0
                yield item
        else:
            item['ClassPicUrl'] = item['productCode'] = item['price'] = item['mainPic'] = item['label'] = item['productName'] = 0
            yield item
