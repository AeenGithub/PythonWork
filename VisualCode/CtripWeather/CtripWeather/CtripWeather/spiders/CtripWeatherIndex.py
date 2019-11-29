# -*- coding: utf-8 -*-
import copy

import scrapy
from CtripWeather.items import CtripweatherItem
from lxml import etree


class CtripweatherindexSpider(scrapy.Spider):
    name = 'CtripWeatherIndex'
    allowed_domains = ['ctrip.com']
    start_urls = ['https://you.ctrip.com/weather/sitemap/place-internal.html']

    def parse(self, response):
        # 省份链接对应表
        province_dict = {}
        ctrip_html = etree.HTML(response.text)
        province_list = ctrip_html.xpath('/html/body/div[3]/div[3]/a')
        for oneprov in province_list:
            province_dict[oneprov.text] = 'https://you.ctrip.com' + oneprov.attrib['href']
        for oneprov, oneprov_url in province_dict.items():
            yield scrapy.Request(
                url=oneprov_url,
                meta={'prov_name': copy.deepcopy(oneprov)},
                callback=self.parse_city
            )

    def parse_city(self, response):
        prov_name = response.meta['prov_name']
        cities_dict = {}
        ctrip_html = etree.HTML(response.text)
        cities = ctrip_html.cssselect('body > div.content > div.w_sitemap_box.w_sitemap_border > ul > li > a')
        for city in cities:
            cities_dict[city.text] = 'https://you.ctrip.com' + city.attrib['href']
        for city_name, city_url in cities_dict.items():
            yield scrapy.Request(
                url = city_url,
                meta={'prov_name': copy.deepcopy(prov_name),
                      'city_name': copy.deepcopy(city_name)},
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = CtripweatherItem()
        prov_name = response.meta['prov_name']
        city_name = response.meta['city_name']
        ctrip_html = etree.HTML(response.text)
        # 标题
        title = ctrip_html.cssselect('div.w_cur_title')[0].text
        # 当前温度
        now_temper = ctrip_html.cssselect('div.w_cur_tem > strong')[0].text
        # 最低温度
        low_temper = ctrip_html.cssselect('div.w_cur_tem > span')[0].text
        # 最高温度
        high_temper = ctrip_html.cssselect('div.w_cur_tem > span > dfn')[0].text
        # 天气状况
        first_weather = ctrip_html.cssselect('div.w_cur_detail > div > p')[0]
        weather = first_weather.text
        # 风速
        wind = first_weather.xpath('text()[2]')[0]
        all_index = ctrip_html.cssselect('div.w_zhishu_city > div > ul > li')
        for one_index in all_index:
            # 获取当前城市所有的生活指数
            index_name = one_index.cssselect('div.w_zhishu_infor > h6')[0].text
            index_clss = one_index.cssselect('div.w_zhishu_infor > strong')[0].text
            index_describe = one_index.cssselect('div.w_zhishu_infor > p')[0].text
            item['prov_name'] = prov_name
            item['city_name'] = city_name
            item['title'] = title
            item['now_temper'] = now_temper
            item['low_temper'] = low_temper
            item['high_temper'] = high_temper
            item['weather'] = weather
            item['wind'] = wind
            item['index_name'] = index_name
            item['index_clss'] = index_clss
            item['index_describe'] = index_describe
            yield item

