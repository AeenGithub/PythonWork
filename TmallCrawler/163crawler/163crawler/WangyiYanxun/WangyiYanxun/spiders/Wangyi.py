# -*- coding: utf-8 -*-
import copy
import json
import re

import scrapy
from WangyiYanxun.items import FirstLevelItem
from lxml import etree


class WangyiSpider(scrapy.Spider):
    name = 'Wangyi'
    allowed_domains = ['163.com']
    start_urls = [
        'http://you.163.com/item/list?categoryId=1005000',
        'http://you.163.com/item/list?categoryId=1008000',
        'http://you.163.com/item/list?categoryId=1010000',
        'http://you.163.com/item/list?categoryId=1043000',
        'http://you.163.com/item/list?categoryId=1010000',
        'http://you.163.com/item/list?categoryId=1013001',
        'http://you.163.com/item/list?categoryId=1005002',
        'http://you.163.com/item/list?categoryId=1005001',
        'http://you.163.com/item/list?categoryId=1011000',
        'http://you.163.com/item/list?categoryId=1019000',
        'http://you.163.com/item/list?categoryId=1065000'
    ]

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        url_detail = 'http://you.163.com/item/detail?id='
        wangyi_html = etree.HTML(response.text)
        firsttitle =  wangyi_html.xpath('/html/head/title/text()')[0]
        wangyi_html.xpath('//script')
        all_page_text = [i.text for i in wangyi_html.xpath(
            '//script') if i.text is not None and 'json' in i.text][0][15:-2]
        json_file = re.findall('{.*?};', all_page_text)[0][:-1]
        json_data = json.loads(json_file)
        categoryItemList = json_data['categoryItemList']
        for one_category in categoryItemList:
            frontDesc = one_category['category']['frontDesc']
            category_id = one_category['category']['id']
            category_name = one_category['category']['name']
            superCategoryId = one_category['category']['superCategoryId']
            for one_item in one_category['itemList']:
                item = FirstLevelItem()
                item['FirstTitle'] = firsttitle
                item['frontDesc'] = frontDesc
                item['category_id'] = category_id
                item['category_name'] = category_name
                item['superCategoryId'] = superCategoryId
                item['colorNum'] = one_item['colorNum']
                item['counterPrice'] = one_item['counterPrice']
                item['item_id'] = one_item['id']
                item['primaryPicUrl'] = one_item['primaryPicUrl']
                item['name'] = one_item['name']
                item['simpleDesc'] = one_item['simpleDesc']
                item['retailPrice'] = one_item['retailPrice']
                item['sellVolume'] = one_item['sellVolume']
                url_detail_id = url_detail + str(item['item_id'])
                yield scrapy.Request(url=url_detail_id, meta={'item': copy.deepcopy(item)}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        detail_html = etree.HTML(response.text)
        detail_page = [i.text for i in detail_html.xpath(
            '//script') if i.text is not None and '详情页数据' in i.text][0][33: -2]
        detail_data = detail_page[:detail_page.find('//其他数据')]
        clear_data = detail_data.replace("\'", '"')
        clear_data = clear_data.replace("\n", '')
        clear_data = clear_data.replace(';', '')
        json_data = json.loads(clear_data)
        for one_attr in json_data['item']['attrList']:
            if '面料' in one_attr['attrName']:
                material = one_attr['attrValue']
                item['material'] = material
            elif '成分' in one_attr['attrName']:
                item['material'] = one_attr['attrValue']
            elif '材质' in one_attr['attrName']:
                item['material'] = one_attr['attrValue']
            else:
                item['material'] = None
            if '风格' in one_attr['attrName']:
                item['style'] = one_attr['attrValue']
            else:
                item['style'] = None
        # yield item
        tag_url = 'http://you.163.com/xhr/comment/tags.json?&itemId=' + \
            str(item['item_id'])
        yield scrapy.Request(url=tag_url, meta={'item': copy.deepcopy(item)}, callback=self.parse_tag)

    def parse_tag(self, response):
        item = response.meta['item']
        item_id = str(item['item_id'])
        json_data = json.loads(response.text)
        tag_comment = []
        for one_tag in json_data['data']:
            if one_tag:
                if one_tag['name'] != '全部' and one_tag['name'] != '有图' and one_tag['name'] != '追评':
                    comment_name = one_tag['name']
                    comment_count = str(one_tag['strCount'])
                    tag_comment.append(comment_name+comment_count)
            else:
                tag_comment.append('')
        item['comment'] = '\t'.join(tag_comment)
        yield item
    #     comment_url = 'http://you.163.com/xhr/comment/listByItemByTag.json?&tag=全部&size=20&page=1&orderBy=0&itemId={}'.format(item_id)
    #     yield scrapy.Request(url=comment_url, meta={'item_id': copy.deepcopy(item_id)}, callback=self.parse_comment)
    #
    # def parse_comment(self, response):
    #     item_id = response.meta['item_id']
    #     json_data = json.loads(response.text)
    #     page = json_data['data']['pagination']['page']
    #     totalPage = json_data['data']['pagination']['totalPage']
    #     for one_page_comment in json_data['data']['result']:
    #         item = CommentItem()
    #         item['item_id'] = item_id
    #         item['frontUserName'] = one_page_comment['frontUserName']
    #         item['content'] = one_page_comment['content']
    #         dtime = datetime.fromtimestamp(one_page_comment['createTime']/1000)
    #         item['createTime'] = dtime.strftime('%Y%m%d %H:%M:%S')
    #         yield item
    #     if page <= totalPage:
    #         next_url = 'http://you.163.com/xhr/comment/listByItemByTag.json?&tag=全部&size=20&page={}&orderBy=0&itemId={}'.format(
    #             page+1, item_id)
    #         yield scrapy.Request(url=next_url, meta={'item_id': copy.deepcopy(item_id)}, callback=self.parse_comment)
