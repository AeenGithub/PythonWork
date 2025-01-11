import scrapy
import copy
import json
import re
from lxml import etree
import time
import math

from scrapy.shell import inspect_response

from PchomeCrawler.items import PchomecrawlerItem
from PchomeCrawler.items import PchomecQtyItem

# e:\文档\Python\TmallCrawler\PchomeCrawler\PchomeCrawler\spiders >

class Pchome24spiderSpider(scrapy.Spider):
    name = 'Pchome24Spider'
    # allowed_domains = ['24h.pchome.com.tw']
    url = 'https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.5/sitemap&fields=Id,Name,Sort,Nodes&_callback=sitemapCategory'

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            dont_filter=True,
            callback=self.parse_sitmap
        )

    def parse_sitmap(self, response):
        # inspect_response(response, self)
        # );}catch(e){if(window.console){console.log(e);}}
        data = json.loads(response.text[20:-48])
        item = PchomecrawlerItem()
        for one_clss in data:
            one_nodes = one_clss['Nodes']
            # 大类，3c，美妆等
            one_clss_id = one_clss['Id']
            one_clss_name = one_clss['Name']
            one_clss_url = one_clss['Url']
            one_clss_sort = one_clss['Sort']
            if one_clss_name not in ['周邊', '美妝保健',  '時尚', '生活', '運動戶外', '家電', '3C',  '書店', '衣鞋包錶', '美妝']:
                for one_node in one_nodes:
                    # 大类，3c，美妆等
                    item['init_clss_id'] = one_clss_id
                    item['init_clss_name'] = one_clss_name
                    item['init_clss_url'] = one_clss_url
                    item['init_clss_sort'] = one_clss_sort
                    # 中类，日用品-五月花，卫生纸等
                    item['init_node_id'] = one_node['Id']
                    item['init_node_name'] = one_node['Name']
                    item['init_node_url'] = one_node['Url']
                    item['init_node_sort'] = one_node['Sort']
                    item['timestamp'] = int(time.time() // 600) * 2
                    second_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/region/{}/menu&_callback=jsonp_nemu&{}?_callback=jsonp_nemu'.format(one_node['Id'], item['timestamp'])
                    yield scrapy.Request(
                        url=second_url,
                        dont_filter=True,
                        callback=self.parse_list_upper,
                        meta={'item': copy.deepcopy(item)}
                    )

    def parse_second_top(self, response):
        # https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.5/region&sign=h24%252F3c&_callback=cb_ecshopCategoryRegion&5332770
        # try{cb_ecshopCategoryRegion(, 28
        item = response.meta['item']
        # inspect_response(response, self)
        print('\n', item['init_clss_id'], response.text[15: 100], '\n')
        # 并不是所有的都能读取理想中的字段，还有其他的，需要判断？？？
        second_data = json.loads(response.text[28:-48])
        for one_clss in second_data:
            item['one_clss_id'] = one_clss['Id']
            item['one_clss_name'] = one_clss['Name']
            item['one_clss_url'] = one_clss['Url']
            item['one_clss_sort'] = one_clss['Sort']
            item['one_clss_isPick'] = one_clss['isPick']
            item['one_clss_isClothing'] = one_clss['isClothing']
            item['timestamp'] = int(time.time() // 600) * 2
            third_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/region/{}/menu&_callback=jsonp_nemu&{}?_callback=jsonp_nemu'.format(one_clss['Id'], item['timestamp'])
            yield scrapy.Request(
                url=third_url,
                dont_filter=True,
                callback=self.parse_list_upper,
                meta={'item': copy.deepcopy(item)}
            )

    # 第三层下半部分（侧边栏），发起总数量的请求
    def parse_list_upper(self, response):
        # https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/region/DSAA/menu&_callback=jsonp_nemu&5332770?_callback=jsonp_nemu
        # try{jsonp_menu(
        item = response.meta['item']
        # inspect_response(response, self)
        lst_data = json.loads(response.text[15:-48])
        for one_clss in lst_data:
            one_clss_id = one_clss['Id']
            one_clss_name = one_clss['Name']
            one_clss_sort = one_clss['Sort']
            one_nodes = one_clss['Nodes']
            for one_node in one_nodes:
                item['second_clss_id'] = one_clss_id
                item['second_clss_name'] = one_clss_name
                item['second_clss_sort'] = one_clss_sort
                item['second_node_id'] = one_node['Id']
                item['second_node_name'] = one_node['Name']
                item['second_node_sort'] = one_node['Sort']
                item['second_node_is24h'] = one_node['is24h']
                item['second_node_isVip'] = one_node['isVip']
                item['second_node_isPick'] = one_node['isPick']
                # 'https://ecapi.pchome.com.tw/ecshop/prodapi/v2/activity/146091/prod/count&_callback=jsonp_prodcount?_callback=jsonp_prodcount'
                count_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{}/prod/count&_callback=jsonp_prodcount?_callback=jsonp_prodcount'.format(item['second_node_id'])
                yield scrapy.Request(
                    url=count_url,
                    dont_filter=True,
                    callback=self.parse_count,
                    meta={'item': copy.deepcopy(item)}
                )

    # 处理总数量请求，处理促销的数量的请求
    def parse_count(self, response):
        item = response.meta['item']
        # inspect_response(response, self)
        count_data = response.text[20:-48]
        item['count_data'] = int(count_data)
        promote_count_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/store/{}/promote&_callback=jsonp_promote&{}?_callback=jsonp_promote'.format(item['second_node_id'], item['timestamp'])
        yield scrapy.Request(
            url=promote_count_url,
            dont_filter=True,
            callback=self.parse_promote_count,
            meta={'item': copy.deepcopy(item)}
        )


    def parse_promote_count(self, response):
        # inspect_response(response, self)
        item = response.meta['item']
        promote_data = json.loads(response.text[18:-48])
        promote_count = promote_data.get('Promote').get('Count')
        item['promote_count'] = int(promote_count)
        # 促销的几个信息下载
        promote_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{}/prod&offset=0&limit={}&fields=Id,Nick,Pic,Price,Discount,isSpec,Name,isCarrier,isSnapUp,isBigCart,OriginPrice,iskdn,isPreOrder24h,PreOrdDate,isWarranty,isFresh,isBidding,isETicket,ShipType,isO2O&_callback=jsonp_prodtop?_callback=jsonp_prodtop'.format(item['second_node_id'], promote_count)
        yield scrapy.Request(
            url=promote_url,
            dont_filter=True,
            callback=self.parse_item_info,
            meta={'item': copy.deepcopy(item)}
        )

        # 列表中各种信息下载
        total_count = item['count_data']
        total_page = math.ceil((total_count - promote_count) / 36)
        if total_page >= 1:
            item['total_page'] = total_page
            for one_page in range(1, total_page + 1):
                item['one_page'] = one_page
                offset = (total_page - 1) * 36 + promote_count + 1
                lst_items_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{}/prod&offset={}&limit=36&fields=Id,Nick,Pic,Price,Discount,isSpec,Name,isCarrier,isSnapUp,isBigCart,OriginPrice,iskdn,isPreOrder24h,PreOrdDate,isWarranty,isFresh,isBidding,isETicket,ShipType,isO2O&_callback=jsonp_prodgrid?_callback=jsonp_prodgrid'.format(item['second_node_id'], offset)
                yield scrapy.Request(
                    url=lst_items_url,
                    dont_filter=True,
                    callback=self.parse_item_info,
                    meta={'item': copy.deepcopy(item)}
                )
        else:
            item['total_page'] = 1
            print('wrong')

    def parse_item_info(self, response):
        item = response.meta['item']
        # inspect_response(response, self)
        begin_text = response.text[:19]
        if 'jsonp_prodtop' in begin_text:
            second_data = json.loads(response.text[18:-48])
        else:
            second_data = json.loads(response.text[19:-48])
        item_id_concat = []
        for one_clss in second_data:
            item['one_item_id'] = one_clss['Id']
            item['one_item_name'] = one_clss['Name']
            item['one_item_nick'] = one_clss['Nick'].replace(',', '')
            item['one_item_price_M'] = one_clss['Price'].get('M')
            item['one_item_price_P'] = one_clss['Price'].get('P')
            item['one_item_price_Prime'] = one_clss['Price'].get('Prime')
            item['one_item_discount'] = one_clss['Discount']
            item_id_concat.append(one_clss['Id'][:16])
            yield item
        id_str = ','.join(item_id_concat)
        qty_promote_url = 'https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id={}&fields=Id,Qty,ButtonType,Price,isPrimeOnly&_callback=jsonp_prodgrid_button?_callback=jsonp_prodgrid_button'.format(
            id_str)
        yield scrapy.Request(
            url=qty_promote_url,
            dont_filter=True,
            callback=self.parse_qty_info,
        )


    def parse_qty_info(self, response):
        # https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id=DSAA6I-A900AT1Q5,DSAA6I-A900ASZB3,DSAA6I-A900ARMHV,DSAA6I-A900A99WA,DSAA6I-A900A364H,DSAA6I-A900A6OFA,DSAA6I-A900AN851,DSAA6I-A900AN0Q5,DSAA6I-A900AKD74,DSAA6I-A900AHUPR,DSAA6I-A900ASZGX,DSAAF8-A900ANE7V,DSAAF8-A900ANE2W&fields=Id,Qty,ButtonType,Price,isPrimeOnly&_callback=jsonp_prodgrid_button?_callback=jsonp_prodgrid_button
        begin_text = response.text[:30]
        if 'jsonp_prodtop' in begin_text:
            qty_data = json.loads(response.text[25:-48])
        else:
            qty_data = json.loads(response.text[26:-48])
        for one_clss in qty_data:
            item = PchomecQtyItem()
            item['qty_id'] = one_clss['Id']
            item['id_qty'] = one_clss['Qty']
            item['price_m'] = one_clss['Price'].get('M')
            item['price_p'] = one_clss['Price'].get('P')
            item['price_prime'] = one_clss['Price'].get('Prime')
            # inspect_response(response, self)
            yield item



    # 表头促销数量
    # https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/store/DSAAC3/promote&_callback=jsonp_promote&5332799?_callback=jsonp_promote
    # 第三层每个类别中的产品数量
    # https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/DSAA4G/prod/count&_callback=jsonp_prodcount?_callback=jsonp_prodcount

    # third_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{}/prod/count&_callback=jsonp_prodcount?_callback=jsonp_prodcount'.format(
    #     one_node['Id'])

    # inspect_response(response, self)


        # print(response.text)

    # scrapy runspider Pchome24Spider.py