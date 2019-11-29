# coding: utf-8

"""
author: Aeenf
"""


# import json
import pickle
import time

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


# from urllib import parse


class GetBrand(object):
    def __init__(self):
        self.url = r'http://qbt.ecdataway.com/brand'
        # options = self.get_drvier_options
        self.brandriver = webdriver.Ie()
        time.sleep(10)
        self.locator = (By.ID, 'header')
        self.month_lst = ['201803', '201804', '201805', '201806', '201807', '201808',
                          '201809', '201810', '201811', '201812', '201901', '201902']
    @property
    def get_drvier_options(self):
        pref_chrome = {
            'profile.default_content_settings.popups': 0,
            'profile.default_content_settings.automaticDownloads': 0,
            "profile.managed_default_content_settings.images": 2,
            'download.default_directory': 'D:\\brand_down\\'}
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_experimental_option('prefs', pref_chrome)
        options.add_extension(
            r"D:\Python\IPython\information\DogAuthExtension.crx")
        return options

    def login_qbt(self):
        """登录成功到情报通网站"""
        self.brandriver.get(r'http://qbt.ecdataway.com/site/login')
        self.brandriver.implicitly_wait(1)
        self.brandriver.find_element_by_id('LoginForm_username').clear()
        self.brandriver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
        self.brandriver.implicitly_wait(1)
        self.brandriver.find_element_by_id('LoginForm_password').send_keys('a123')
        self.brandriver.find_element_by_class_name('login_btn').click()
        try:
            print('正在登录……')
            WebDriverWait(self.brandriver, 5).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
        except exceptions.TimeoutException as e:
            print(e)
            print('登录缓慢，请稍后……')
        return '登录成功！'

    def get_lst_of_brand(self):
        """根据指定的url选择所关注的20家品牌商的相关信息"""
        attribute = {}
        self.brandriver.get(self.url)
        try:
            WebDriverWait(self.brandriver, 6).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
        #     time.sleep(10)
        except Exception as e:
            print('1', e)
        all_href = self.brandriver.find_elements_by_css_selector('#set1 > tbody > tr > td > a')
        for link in all_href:
            try:
                href = link.get_attribute('href')
                if 'brand' in href:
                    name = link.text
                    attribute[name] = href
            except TypeError as e:
                pass
        print('店铺列表和链接获取成功')
        return attribute

    def sidebar_category(self, brand_url):
        """获取指定店铺的大类列表"""
        class_of_sexandboy = {}
        self.brandriver.get(brand_url)
        try:
            WebDriverWait(self.brandriver, 6).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
        #     time.sleep(1)
        except exceptions.TimeoutException as e:
            self.login_qbt()
            self.sidebar_category(brand_url)
            print('2', e)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector(
            '#sidebar_category > ul > li > a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'brand' in href:
                class_of_sexandboy[category.text] = href
        print('大类清单获取成功')
        return class_of_sexandboy

    def sidebar_category_second(self, midclss_url):
        """获取指定店铺的中类列表"""
        class_of_clothe = {}
        self.brandriver.get(midclss_url)
        try:
            WebDriverWait(self.brandriver, 6).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
        #     time.sleep(1)
        except exceptions.TimeoutException as e:
            print('3', e)
            self.login_qbt()
            self.sidebar_category_second(midclss_url)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector(
            '#sidebar_category > ul > li > a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'brand' in href:
                class_of_clothe[category.text] = href
        print('中类清单获取成功')
        return class_of_clothe

    def clothe_element(self, clothe_element_url):
        """获取指定中类的元素列表"""
        class_of_clothe = {}
        self.brandriver.get(clothe_element_url)
        try:
            WebDriverWait(self.brandriver, 6).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
        #     time.sleep(1)
        except exceptions.TimeoutException as e:
            print('3', e)
            self.login_qbt()
            self.clothe_element(clothe_element_url)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector(
            '#sidebar_category > ul > li > a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'brand' in href:
                class_of_clothe[category.text] = href
        print('中类清单获取成功')
        return class_of_clothe

    def get_link_excel(self):
        """通过三层访问，获取每一个品牌的链接、大类链接和中类链接"""
        brand_df_concat = []
        all_brand_lst = self.get_lst_of_brand()
        for one_brand in all_brand_lst.items():
            brand_name, brand_url = one_brand
            one_brand_midclss = self.sidebar_category(brand_url).items()
            for one_midclss in one_brand_midclss:
                midclss, midclss_url = one_midclss
                clothe_clss = self.sidebar_category_second(midclss_url)
                # 获取一个品牌下的一个大类的链接清单
                df_clothe_clss = pd.DataFrame(clothe_clss, index=['clothe_link']).transpose().reset_index()
                df_clothe_clss['brand_name'] = brand_name
                df_clothe_clss['brand_link'] = brand_url
                df_clothe_clss['midclss'] = midclss
                df_clothe_clss['midclss_url'] = midclss_url
                brand_df_concat.append(df_clothe_clss)
        brand_df = pd.concat(brand_df_concat, ignore_index=True)
        brand_df.to_excel('brand_senior_link.xlsx')
        with open('brand_senior', 'wb') as f:
            f.write(pickle.dumps(brand_df))
        return 'all is ok'

    def get_one_category_detail(self, url_cagory, month):
        """通过url访问单个中类单月的top宝贝信息"""
        url_trend = url_cagory + '&type=4#fold_line'
        try:
            self.brandriver.get(url_trend)
            WebDriverWait(self.brandriver, 3).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
            time.sleep(1)
            period_start = Select(self.brandriver.find_element_by_id('period'))
            period_start.select_by_value(month)
            period_last = Select(
                self.brandriver.find_element_by_id('period_last'))
            period_last.select_by_value(month)
        except exceptions.TimeoutException as e:
            print('访问热销宝贝', e)
            self.brandriver.refresh()
        except Exception:
            self.login_qbt()
            self.get_one_category_detail(url_cagory, month)
        try:
            self.brandriver.find_element_by_id('submit-button').click()
            WebDriverWait(self.brandriver, 30).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
            time.sleep(2)
        except exceptions.TimeoutException as e:
            print('下载热销宝贝', e)
            self.brandriver.refresh()
        except Exception:
            self.login_qbt()
            self.get_one_category_detail(url_cagory, month)
            time.sleep(2)
        # self.brandriver.execute_script(js)
        # time.sleep(5)
        return '     {}文件检索成功'.format(month)

    def got_file_from_web(self, brand_name, month, clothe_clss, midclss):
        """将数据从网页上获取，处理成dataframe"""
        thead = self.brandriver.find_elements_by_css_selector(
            '#content > div.charts > div > div.grid-view > table > thead')[0].text
        # print(thead.split(' '))
        picture = self.brandriver.find_elements_by_css_selector(
            '#content > div.charts > div > div.grid-view > table > tbody > tr > td > img')
        img_lst = []
        for one in picture:
            img_url = one.get_attribute('src')
            if 'jpg' in img_url:
                img_lst.append(img_url)
        img_df = pd.DataFrame(img_lst)
        tbody = self.brandriver.find_elements_by_css_selector(
            '#content > div.charts > div > div.grid-view > table > tbody')[0]
        reptext = tbody.text.replace(', ', '&').split('\n')
        tbody_text = []
        for i in reptext:
            one_row = i.split(' ')
            a = len(one_row) - 8
            if a >= 1:
                one_row_s = one_row[a:]
            else:
                one_row_s = one_row
            tbody_text.append(one_row_s)
        tbody_link = self.brandriver.find_elements_by_css_selector(
            '#content > div.charts > div > div.grid-view > table > tbody > tr > td> a')
        item_id = [[one.text, one.get_attribute(
            'href')] for one in tbody_link if 'id' in one.get_attribute('href')]
        one_table = pd.DataFrame(tbody_text, columns=thead.split(' '))
        item_id_df = pd.DataFrame(item_id, columns=['宝贝名称', '宝贝链接'])
        last_table = pd.concat([item_id_df, one_table, img_df], axis=1)
        last_table['brand_name'] = brand_name
        last_table['clothe_clss'] = clothe_clss
        last_table['month'] = month
        last_table['midclss'] = midclss
        last_table.to_excel('D:\\情报通shop\\{0}_{1}_{2}_{3}.xls'.format(
            brand_name, midclss, clothe_clss.replace('/', '&'), month))
        print('    {0}_{1}_{2}_{3}保存成功'.format(brand_name,
                                               midclss, clothe_clss.replace('/', '&'), month))
        return last_table

    def main(self):
        with open('brand_senior', 'rb') as f:
            df_brand = pickle.loads(f.read())
        print(self.login_qbt())
        for one_category in df_brand.values:
            clothe_clss = one_category[0].replace('/', '')
            clothe_url = one_category[1]
            brand_name = one_category[2].replace('/', '')
            midclss = one_category[4].replace('/', '')
            print(brand_name, '正在访问------')
            print('    ', clothe_clss, '正在下载')
            concat_df = pd.DataFrame()
            for month in self.month_lst:
                time.sleep(2)
                print(self.get_one_category_detail(clothe_url, month))
                try:
                    one_month_table = self.got_file_from_web(
                        brand_name, month, clothe_clss, midclss)
                except Exception:
                    one_month_table = None
                concat_df = concat_df.append(one_month_table)
                concat_df.to_csv('汇总.csv', mode='a')
                one_row = '    '.join([brand_name, clothe_clss, clothe_url])
                with open("D:\\shop_url.txt", 'a', encoding='utf-8') as f:
                    f.write(one_row)
                    f.write('\n')
                continue
        print('所有的店铺均已完成')
        self.brandriver.quit()
        return '运行结束'


if __name__ == "__main__":
    brand_detail = GetBrand()
    print(brand_detail.main())
    # print(brand_detail.login_qbt())
    # print(brand_detail.get_link_excel())
