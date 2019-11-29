# coding: utf-8

"""
author: Aeenf
"""

import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class QbtShopAnalyse(object):
    def __init__(self):
        options = self.get_drvier_options
        self.shopdriver = webdriver.Chrome(options=options)
        self.locator = (By.ID, 'header')
        self.content = (By.ID, 'content')
        self.shop_url = r'http://qbt.ecdataway.com/shop?page'

    @property
    def get_drvier_options(self):
        """对Chrome进行配置"""
        pref_chrome = {
            'profile.default_content_settings.popups': 0,
            'profile.default_content_settings.automaticDownloads': 0,
            "profile.managed_default_content_settings.images": 2,
            'download.default_directory': 'E:\\brand_down\\'
        }
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_experimental_option('prefs', pref_chrome)
        options.add_extension(r"D:\Python\Scode\情报通\DogAuthExtension.crx")
        return options

    def qbt_login(self):
        """登录成功到情报通网站"""
        try:
            print('正在登录……')
            self.shopdriver.get(r'http://qbt.ecdataway.com/site/login')
            self.shopdriver.implicitly_wait(1)
            self.shopdriver.find_element_by_id('LoginForm_username').clear()
            self.shopdriver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
            self.shopdriver.implicitly_wait(1)
            self.shopdriver.find_element_by_id('LoginForm_password').send_keys('a123')
            self.shopdriver.find_element_by_class_name('login_btn').click()
            WebDriverWait(self.shopdriver, 10).until(EC.presence_of_element_located(self.locator))
            self.shopdriver.implicitly_wait(5)
        except exceptions.TimeoutException as e:
            print(e)
            print('登录缓慢，请稍后……')
        except Exception:
            print('登录异常，重新登录')
            self.qbt_login()
        return '登录成功！'

    def get_shop_lst(self):
        """获取所有的店铺列表"""
        one_page_shoplink_df = []
        for page_num in [1, 2]:
            one_page_shoplink = []
            self.shopdriver.get('{}={}'.format(self.shop_url, page_num))
            shoplst_df = pd.read_html(self.shopdriver.page_source)[0]
            shoplst = self.shopdriver.find_elements_by_xpath('//*[@id="tag-flag"]/tr')
            for one_shop in shoplst:
                shop_name = one_shop.find_elements_by_css_selector('tr > td > a')[0].text
                itemlst_url = one_shop.find_elements_by_css_selector('tr > td > div > a')[0].get_attribute('href')
                one_page_shoplink.append((shop_name, itemlst_url))
            one_page_shop_item_link = pd.DataFrame(one_page_shoplink, columns=['掌柜名称', '宝贝链接'])
            one_page_all_link = shoplst_df.merge(one_page_shop_item_link, left_on='掌柜名称', right_on='掌柜名称')
            one_page_shoplink_df.append(one_page_all_link)
        last_shop_link = pd.concat(one_page_shoplink_df)
        last_shop_link.to_excel('e:\\店铺列表.xlsx')
        return last_shop_link[['掌柜名称', '宝贝数量', '宝贝链接']].values

    def get_one_shop_one_page(self, one_page, shop_url):
        """先根据宝贝数量和每页宝贝数量101，计算页数，然后分页抓取数据"""
        print('\t第{}页数据正在抓取'.format(one_page))
        # 利用Chrome抓取每一页的数据
        self.shopdriver.get('{}&page={}'.format(shop_url, one_page))
        WebDriverWait(self.shopdriver, 6).until(EC.presence_of_element_located(self.content))
        self.shopdriver.implicitly_wait(6)
        time.sleep(1)
        # 利用pandas的接口解析网页
        try:
            one_page_data = pd.read_html(self.shopdriver.page_source)[0]
            # 修改抓取数据的表头
            one_page_data.columns = ['其他',
                                     '宝贝名称',
                                     '商品类别',
                                     '品牌',
                                     '参考价格',
                                     '成交均价-本月',
                                     '成交均价-上月',
                                     '折扣率-本月',
                                     '折扣率-上月',
                                     '销量-本月',
                                     '销量-上月',
                                     '销售额-本月',
                                     '销售额-上月',
                                     '更新时间',
                                     'pass']
            one_page_data.dropna(thresh=10, inplace=True)
            # 获取商品图片的链接
            one_page_picture_link = [i.get_attribute('src') for i in self.shopdriver.find_elements_by_css_selector(
                '#content > div.grid-view > form > table > tbody > tr > td > img')]
            one_page_item_link = [i.get_attribute('href') for i in self.shopdriver.find_elements_by_css_selector('#content > div.grid-view > form > table > tbody > tr > td:nth-child(2) > a')]
            one_page_data['商品链接'] = one_page_picture_link
            one_page_data['宝贝地址'] = one_page_item_link
            one_page_data.dropna(axis=1, how='any', inplace=True)
            return one_page_data
        except IndexError as e:
            print('当前页数据无法显示，无法抓取', e)
            self.shopdriver.refresh()
            self.get_one_shop_one_page(one_page, shop_url)
        except  exceptions.TimeoutException as e:
            print('重新登录', e)
            self.qbt_login()
            self.get_one_shop_one_page(one_page, shop_url)

    def qbt_main(self):
        lst_df = pd.read_excel(r'e:\店铺列表2.xlsx')
        shop_data = lst_df[['掌柜名称', '宝贝数量', '宝贝链接']].values
        for shop_name, total_count, shop_link in shop_data:
            if Path('E:\\shop_down\\{}.xlsx'.format(shop_name)).exists():
                print('{}数据已经存在，下一个'.format(shop_name))
            else:
                print('{}共有{}个宝贝'.format(shop_name, total_count))
                all_pages = total_count//100+1
                all_page_lst = []
                for one_page in range(1, all_pages+1):
                    print('\t第{}页正在下载'.format(one_page))
                    one_page_data = self.get_one_shop_one_page(one_page, shop_link)
                    all_page_lst.append(one_page_data)
                    print('\t第{}页下载完成\n'.format(one_page))
                all_pages_data = pd.concat(all_page_lst, ignore_index=True, sort=True)
                all_pages_data.to_excel('E:\\shop_down\\{}.xlsx'.format(shop_name))
        print('所有店铺均已经完成')
        self.shopdriver.quit()


if __name__=='__main__':
    qbt_shop = QbtShopAnalyse()
    qbt_shop.qbt_login()
    qbt_shop.qbt_main()

