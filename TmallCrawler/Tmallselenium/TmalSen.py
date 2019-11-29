# coding: utf-8

import csv
import time
from datetime import datetime
from urllib import request

# from selenium.webdriver.support.ui import WebDriverWait
import matplotlib.pyplot as plt
from PIL import Image
from selenium import webdriver
from selenium.common import exceptions


class TmallSen(object):
    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Firefox()
        datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.title = ['store_name', 'item_id', 'price', 'quantity', 'title', 'totalSoldQuantity', 'url', 'img']
        self.filename = 'D:\\Python\\TmallCrawler\\file\\{}_{}.csv'.format('store_of_Tmall', datenum)
        self.get_file()

    def get_file(self):
        '''创建一个含有标题的表格'''
        with open(self.filename, 'w', newline='', encoding='gbk') as f:
            writer = csv.DictWriter(f, fieldnames=self.title)
            writer.writeheader()
        return '表格创建成功'

    def get_one_url(self):
        """从文件获取需要爬取的url链接"""
        url_file = r"D:\Python\TmallCrawler\file\Tamll_shop_sen"
        with open(url_file, 'r', encoding='utf-8') as f:
            csv_reader = f.read().split('\n')
            for row in csv_reader:
                yield row.split('\t')

    def tmall_login(self):
        self.driver.get('https://login.tmall.com/')
        iii = self.driver.find_element_by_id('J_loginIframe')
        self.driver.implicitly_wait(3)
        self.driver.get(iii.get_attribute('src'))
        code_url = self.driver.find_element_by_css_selector('#J_QRCodeImg > img').get_attribute('src')
        request.urlretrieve(code_url, 'code.png')
        img = Image.open('code.png')
        plt.imshow(img)
        plt.show()
        print('登录成功')

    def one_shop(self, name, url):
        title = ['store_name', 'item_id', 'price', 'quantity', 'title', 'totalSoldQuantity', 'url', 'img']
        page_num = 1
        while True:
            category_url = url + '/category.htm?orderType=defaultSort&pageNo=' + str(page_num) + '#anchor'
            self.driver.get(category_url)
            self.driver.implicitly_wait(3)
            # try:
            #     self.driver.find_element_by_css_selector('#J_ShopSearchResult > div > div.J_TItems > div.pagination > a.disable').text == '下一页'
            #     self.driver.implicitly_wait(3)
            #     break
            # except:
            page_cur = self.driver.find_element_by_css_selector('#J_ShopSearchResult > div > div.J_TItems > div.pagination > a.page-cur').text
            # page_cur = self.driver.find_element_by_class_name('page_cur').text
            print('当前页面是--', page_cur, '--页')
            items = self.driver.find_elements_by_class_name('item ')
            for one_item in items[:-2]:
                self.driver.implicitly_wait(3)
                try:
                    item_id = one_item.get_attribute('data-id')
                    img_url = one_item.find_element_by_tag_name('img').get_attribute('src')
                    title = one_item.find_element_by_tag_name('img').get_attribute('alt')
                    detail_url = one_item.find_element_by_tag_name('a').get_attribute('href')
                    price = one_item.find_element_by_class_name('c-price').text
                    sale_num = one_item.find_element_by_class_name('sale-num').text
                    comment = one_item.find_element_by_tag_name('h4').text
                    url = 'https://detail.tmall.com/item.htm?id='+item_id
                    # self.driver.get(detail_url)
                    # sold = self.driver.find_element_by_class_name('tm-count').text
                    # products = {
                    #         'store_name': '优衣库',
                    #         'item_id': item_id,
                    #         'price': price,
                    #         'quantity': comment,
                    #         'title': title,
                    #         'totalSoldQuantity': sale_num,
                    #         'url': 'https://detail.tmall.com/item.htm?id='+item_id,
                    #         'img': img_url
                    #     }
                    # print(products)
                    pro = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(name, item_id, price, comment, title, sale_num, detail_url, img_url)
                    print(pro)
                    with open('d:\\Test\\data.txt', 'a', encoding='gbk', errors='ignore') as f:
                        # writer = csv.DictWriter(f, fieldnames=self.title)
                        # writer.writerow(products)
                        f.write(pro)
                except (exceptions.StaleElementReferenceException, exceptions.NoSuchElementException):
                    print('数据下载完毕')
                    pass
            page_num += 1
            return 'all is ok'

    def main(self):
        self.tmall_login()
        time.sleep(10)
        for shopname_url in self.get_one_url():
            store_name = shopname_url[0]
            print(store_name, '正在访问')
            store_url = shopname_url[1]
            print(self.one_shop(store_name, store_url))

if __name__ == '__main__':
    Tmallspider = TmallSen()
    Tmallspider.main()