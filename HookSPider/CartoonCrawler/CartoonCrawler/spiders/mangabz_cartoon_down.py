import copy
import json
import re
import urllib.parse as uparse
import logging

import scrapy
# debug
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser

from CartoonCrawler.items import CartooncrawlerItem
from lxml import etree
logger = logging.getLogger('mangabz_logger')

class CartoonCrawler(scrapy.Spider):
    name = 'mangabz'
    allowed_domains = ['mangabz.com']


    def start_requests(self):
        init_url = 'https://www.mangabz.com/38bz/'
        yield scrapy.Request(
            url = init_url,
            method = 'GET',
            callback = self.parse
        )

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = CartooncrawlerItem()
        html = etree.HTML(response.text)
        chapterlistload = html.xpath('//*[@id="chapterlistload"]')[0]
        chapters = chapterlistload.xpath('//*[@id="chapterlistload"]/a["href"]')
        '每一章的循环'
        for one_chapter in chapters:
            one_chapter_text = re.sub("[^\u4e00-\u9fa5a-zA-Z0-9]", "", one_chapter.text)
            item['title'] = one_chapter_text
            item['url'] = 'https://www.mangabz.com/' + one_chapter.get('href')
            yield scrapy.Request(
                url=item['url'],
                method='GET',
                meta={'item': copy.deepcopy(item)},
                callback = self.parse_chapter
            )

    def parse_chapter(self, response):
        # cartoon_html = etree.HTML(response.text)
        item = response.meta['item']
        # re_title = re.findall(r'<title>(.*)</title>',response.text)
        re_vars = re.findall(r'(var.*?;)', response.text)
        for one_var in re_vars:
            # var MANGABZ_CURL = "/m7261/";',
            one_var_row = [i.replace('"','').replace(' ', '') for i in one_var[4:-1].split('=')]
            # print(one_var_row)
            if 'MANGABZ_CURL' == one_var_row[0]:
                item['curl'] = one_var_row[1]
            if 'MANGABZ_IMAGE_COUNT' == one_var_row[0]:
                item['count'] = one_var_row[1]
            if 'MANGABZ_CTITLE' == one_var_row[0]:
                item['init_title'] = one_var_row[1]
            if 'MANGABZ_PAGEINDEX' == one_var_row[0]:
                item['init_index'] = one_var_row[1]
            if 'MANGABZ_VIEWSIGN' == one_var_row[0]:
                item['viewsign'] = one_var_row[1]
            if 'MANGABZ_VIEWSIGN_DT' == one_var_row[0]:
                item['viewsign_time'] = one_var_row[1]
            if 'MANGABZ_MID' == one_var_row[0]:
                item['mid'] = one_var_row[1]
            if 'MANGABZ_CID' == one_var_row[0]:
                item['cid'] = one_var_row[1]
        # print(re_vars)
        # print(item)
        # item['re_vars'] = re_vars
        carton_detail = 'https://www.mangabz.com/m7261/chapterimage.ashx'
        # 一章漫画内部有多页，多页循环
        for cindex in range(1, int(item['count'])):
            item['cindex'] = cindex
            params_data = {
                'cid': item['cid'],
                'page': cindex,
                'key': '',
                '_cid': item['cid'],
                '_mid': item['mid'],
                '_dt': item['viewsign_time'],
        }
            carton_detail_url = carton_detail + '?' + uparse.urlencode(params_data, encoding='utf-8')
            # print(carton_detail_url)
            yield scrapy.Request(
                method='GET',
                url=carton_detail_url,
                cb_kwargs={'item': copy.deepcopy(item)},
                callback=self.parse_detail)
    
    def parse_detail(self, response, item):
        # inspect_response(response, self)
        # 通过对返回的内容解析，获取图片链接
        pattern = "\d{1,},\d{1,},'\|\|(.*)"
        res_str = re.findall(pattern, response.text)
        if not res_str:
            logger.info('res_lst: %s', res_str)
            # open_in_browser(response)
            inspect_response(response, self)
        else:
            res_str = res_str[0]
            pic_res_lst = res_str.split('|')
            # logger.info('res_lst: %s', res_lst)

            # "https://image.mangabz.com/1/38/7262/2_1285.jpg?cid=7262&key=d234d6bc54236344c62439556e4e7443&uk="
            image_init_url = 'https://image.mangabz.com/1/' + item['mid'] + '/' + item['cid'] + '/'
            # logger.info(pic_res_lst)

            # 图片链接中的key值是个32位的加密参数，由此获得
            ikey = [i_conte for i_conte in pic_res_lst if len(i_conte) == 32]
            if ikey:
                ikey = ikey[0]
            else:
                inspect_response(response, self)

            # 由于每一页可能会有多张图片，所以内部再循环
            cartoon_seq = []
            for i_conte in pic_res_lst:
                # logger.info(i_conte)
                # 翻页后每张图片的名称大致是：序号_四位数字，从垃圾信息中进行提取
                # 由于垃圾信息顺序难以保证，需要额外处理，根据返回值的构成，序号_四位数字，是不是序号就是顺序呢？
                if i_conte[-4:].isdigit() and '_' in i_conte:
                    cartoon_seq.append((ikey, i_conte))
            # print(cartoon_seq)
            # logger.info('cartoon_seq: %s', cartoon_seq)
            for i, icontent in enumerate(cartoon_seq):
                ikey, one_seq = icontent
                if one_seq.split('_')[0] == str(item['cindex']):
                    image_url = image_init_url + one_seq + '.jpg?cid=' + item['cid'] + '&key=' + ikey + '&uk='
                    item['ikey'] = ikey
                    item['index'] = i
                    item['one_seq'] = one_seq
                    item['image_url'] = image_url
                    # logger.info('item: %s', item)
                    yield item
        # print(test)
        # yield item
        
