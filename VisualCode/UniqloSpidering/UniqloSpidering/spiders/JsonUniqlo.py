# -*- coding: utf-8 -*-
import copy
import json
import math

import scrapy
from UniqloSpidering.items import UniqloDetailItem, UniqloJsonItem, UniqlocategoriesItem


class JsonuniqloSpider(scrapy.Spider):
    name = 'JsonUniqlo'
    allowed_domains = ['uniqlo.cn']
    start_urls = ['http://www.uniqlo.cn/']
    json_headers = {
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Connection': "keep-alive",
        'Host': "www.uniqlo.cn",
        'Referer': "https://www.uniqlo.cn/women_heattech.html",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
    }

    def start_requests(self):
        json_url = "https://www.uniqlo.cn/data/cms-config.json"
        yield scrapy.Request(
            url=json_url,
            headers=self.json_headers
        )

    def parse(self, response):
        new_headers = self.json_headers
        add_headers = {
            'Connection': "keep-alive",
            'Content-Length': "315",
            'Content-Type': "application/json",
            'Host': "d.uniqlo.cn",
            'Origin': "https://www.uniqlo.cn",
        }
        new_headers.update(add_headers)
        json_data = json.loads(response.text)
        json_pages = json_data['pages']
        json_category = json_data['categories']
        for one_page in json_pages:
            item = UniqloJsonItem()
            item['path'] = 'https://www.uniqlo.cn' + one_page['path']
            item['tplt'] = one_page['tplt']
            item['backgroundFit'] = one_page.get('backgroundFit')
            item['components'] = one_page['components']
            item['superCode'] = one_page['superCode']
            item['backgroundFixed'] = one_page.get('backgroundFixed')
            item['title'] = one_page['title']
            yield item
        for one_category in json_category:
            fexpand = one_category['expand']
            fcode = one_category['code']
            fparentCode = one_category['parentCode']
            fname = one_category['name']
            fsort = one_category['sort']
            categories = one_category.get('categories')
            if categories:
                for next_categories in categories:
                    item = UniqlocategoriesItem()
                    item['fexpand'] = fexpand
                    item['fcode'] = fcode
                    item['fparentCode'] = fparentCode
                    item['fname'] = fname
                    item['fsort'] = fsort
                    item['expand'] = next_categories['expand']
                    item['code'] = next_categories['code']
                    item['parentCode'] = next_categories['parentCode']
                    item['name'] = next_categories['name']
                    item['sort'] = next_categories['sort']
                    CategoryCode = copy.deepcopy(item['code'])
                    yield item
                    new_headers['Referer'] = 'https://www.uniqlo.cn/c/{}.html'.format(CategoryCode)
                    yield scrapy.Request(
                        url='https://d.uniqlo.cn/hmall-sc-service/search/searchWithCategoryCodeAndConditions/zh_CN',
                        method='POST',
                        body='{"url":"/c/%s.html","pageInfo":{"page":1,"pageSize":24,"withSideBar":"Y"},"belongTo":"pc","rank":"overall","priceRange":{"low":0,"high":0},"color":[],"size":[],"season":[],"material":[],"sex":[],"identity":[],"insiteDescription":"","exist":[],"categoryCode":"%s","searchFlag":"false","description":""}' % (
                            CategoryCode, CategoryCode),
                        meta={'CategoryCode': CategoryCode},
                        dont_filter=True,
                        headers=new_headers,
                        callback=self.parse_pages
                    )
    def parse_pages(self, response):
        Code = response.meta['CategoryCode']
        new_headers = self.json_headers
        add_headers = {
            'Connection': "keep-alive",
            'Content-Length': "315",
            'Content-Type': "application/json",
            'Host': "d.uniqlo.cn",
            'Origin': "https://www.uniqlo.cn",
        }
        new_headers.update(add_headers)
        json_data = json.loads(response.text)
        resp = json_data['resp']
        productSum = resp[2]['productSum']
        pageSize = resp[2]['pageSize']
        total_page = math.ceil(float(productSum)/pageSize)
        for page in range(1, total_page+1):
            CategoryCode = copy.deepcopy(Code)
            new_headers['Referer'] = 'https://www.uniqlo.cn/c/{}.html'.format(CategoryCode)
            yield scrapy.Request(
                url='https://d.uniqlo.cn/hmall-sc-service/search/searchWithCategoryCodeAndConditions/zh_CN',
                method='POST',
                body='{"url":"/c/%s.html?page=%s","pageInfo":{"page":%s,"pageSize":24,"withSideBar":"Y"},"belongTo":"pc","rank":"overall","priceRange":{"low":0,"high":0},"color":[],"size":[],"season":[],"material":[],"sex":[],"identity":[],"insiteDescription":"","exist":[],"categoryCode":"%s","searchFlag":"false","description":""}' % (
                    CategoryCode, page, page, CategoryCode),
                # meta={'item': copy.deepcopy(item)},
                dont_filter=True,
                headers=new_headers,
                callback=self.parse_merchandise
            )
    def parse_merchandise(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text)
        MerchandiseLst = json_data['resp'][1]
        first_category_code = json_data['resp'][3][0]['categoryCode']
        first_category_name =  json_data['resp'][3][0]['categoryName']
        second_category_code = json_data['resp'][3][1]['categoryCode']
        second_category_name = json_data['resp'][3][1]['categoryName']
        for onemer in MerchandiseLst:
            item = UniqloDetailItem()
            item['first_category_code'] = first_category_code
            item['first_category_name'] = first_category_name
            item['second_category_code'] = second_category_code
            item['second_category_name'] = second_category_name
            item['productName'] = onemer['productName']
            item['littlecode'] = onemer['code']
            item['sales'] = onemer['sales']
            item['mainPic'] = onemer['mainPic']
            item['season'] = onemer['season']
            item['originPrice'] = onemer['originPrice']
            item['preSaleName'] = onemer['preSaleName']
            item['littlename'] = onemer['name']
            item['minPrice'] = onemer['minPrice']
            item['sex'] = onemer['sex']
            item['styleText'] = onemer['styleText']
            item['material'] = onemer['material']
            item['categoryCode'] = onemer[ 'categoryCode']
            item['productCode'] = onemer['productCode']
            item['label'] = onemer['label']
            item['size'] = onemer['size']
            yield item

