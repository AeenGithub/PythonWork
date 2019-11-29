# coding:utf-8
import json
import time
from datetime import datetime
from random import randint

import pandas as pd
import requests


class UniqloStore(object):
    # 设置初始的配置文件，如header， url等
    def __init__(self):
        self.datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.first_url = r'https://d.uniqlo.cn/hmall-sc-service/search/searchWithConditions4StoreOnly/zh_CN'
        self.uniqlo_headers = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Authorization': "",
            'Connection': "keep-alive",
            'Content-Length': "200",
            'Content-Type': "application/json",
            'Host': "d.uniqlo.cn",
            'Origin': "https://h.uniqlo.cn",
            'Referer': "https://h.uniqlo.cn/",
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }

    # 对post的内容进行编码
    def post_params(self, page):
        post_params = {
            "pageInfo": {"page": page, "pageSize": 16},
            "storeCode": "105403",
            "insiteDescription": "",
            "color": [],
            "size": [],
            "season": [],
            "material": [],
            "identity": [],
            "sex": [],
            "rank": "overall",
            "priceRange": {"low": 0, "high": 0}
        }
        return post_params

    # 进行post请求
    def request_post(self, page):
        page_data = json.dumps(self.post_params(page))
        # print(page_data)
        result = requests.post(
            url=self.first_url,
            headers=self.uniqlo_headers,
            data=page_data)
        return result.text

    # 对post结果进行解析
    def deal_json(self, page):
        deal_json_data = self.request_post(page)
        json_data = json.loads(deal_json_data)
        response_data = json_data['resp']
        item_clss = response_data[0]
        product_lst = response_data[1]
        product_info = response_data[2]
        return item_clss, product_lst, product_info

    # 联系各个方法，进行循环爬取
    def main(self):
        page = 1
        xlsx_writer = pd.ExcelWriter('D:\\文档\\A天猫\\优衣库专题\\优衣库门店\\淮海路旗舰店_{}.xlsx'.format(self.datenum))
        item_clss, product_lst, product_info = self.deal_json(page)
        total_page = int(product_info['productSum'])//16 + 1
        pages_lst = []
        for one_page in range(1, total_page+1):
            time.sleep(randint(5, 10))
            print('一共有{}页，{}页正在访问中，请稍等……'.format(total_page, one_page))
            item_clss, product_lst, product_info = self.deal_json(one_page)
            pages_lst.extend(product_lst)
            print('一共有{}页, {}页下载完成\n'.format(total_page, one_page))
        df_item_clss = pd.DataFrame(item_clss)
        df_item_clss.to_excel(xlsx_writer, sheet_name='分类逻辑')
        df_product_lst = pd.DataFrame(pages_lst)
        df_product_lst.to_excel(xlsx_writer, sheet_name='产品列表')
        df_product_info = pd.DataFrame(product_info, index=['0'])
        df_product_info.to_excel(xlsx_writer, sheet_name='总数据')
        xlsx_writer.save()


if __name__ == '__main__':
    uniqlo_spider = UniqloStore()
    print(uniqlo_spider.main())
