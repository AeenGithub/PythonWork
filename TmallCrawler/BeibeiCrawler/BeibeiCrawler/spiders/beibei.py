# -*- coding: utf-8 -*-
import copy
import json

import scrapy
from BeibeiCrawler.items import BeibeicrawlerItem


class BeibeiSpider(scrapy.Spider):
    name = 'beibei'
    allowed_domains = ['beibei.com']
    start_urls = ['https://dsapi.beibei.com/martshow/home/channel/7702-1-bab\
    ythings-1000.html?client_info=undefined&h5_uid=undefined']

    def parse(self, response):
        json_data = json.loads(response.text)
        page = json_data['page']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        page_size = json_data['page_size']
        total_count = json_data['total_count']
        totalpage = total_count//page_size + 1
        # print(totalpage)
        for page in range(1, 46):
            url = 'https://dsapi.beibei.com/martshow/home/channel/7702-{}-bab\
            ythings-1000.html?client_info=undefined&h5_uid=unde\
            fined'.format(str(page))
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        json_data = json.loads(response.text)
        page = json_data['page']
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for one_rows in json_data['martshows']:
            try:
                one_items = one_rows['type_home_item_double']['items']
                for one_item in one_items:
                    item = BeibeicrawlerItem()
                    item['page'] = page
                    item['iid'] = one_item['iid']
                    item['buying_info'] = one_item['buying_info']
                    item['img'] = one_item['img']
                    item['title'] = one_item['title']
                    item['sale_num'] = one_item['sale_num']
                    item['price'] = one_item['price']
                    item['origin_price'] = one_item['origin_price']
                    item['stock'] = one_item['stock']
                    tag_url = 'https://sapi.beibei.com/item/rate/0-{}-1-10.html?\
                    callback=BeibeiItemRateGet'.format(str(one_item['iid']))
                    # yield item
                    yield scrapy.Request(
                        url=tag_url,
                        callback=self.parse_tag,
                        meta={'item': copy.deepcopy(item)}
                    )
            except KeyError:
                pass

    def parse_tag(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        json_data = json.loads(response.text[18:-1])
        item = response.meta['item']
        item['CommentCount'] = json_data['count']
        item['default_praise_count'] = json_data['default_praise_count']
        item['favorRate'] = json_data['favourable_comment']['rate']
        tags = []
        for one_tag in json_data['rate_tags']:
            if one_tag['name'] != '晒图':
                one = one_tag['name'] + '|' + str(one_tag['count'])
                tags.append(one)
        item['tags'] = '\t'.join(tags)
        yield item
