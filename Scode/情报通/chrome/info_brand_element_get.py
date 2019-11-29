# coding: utf-8

"""
author: Aeenf
"""

import pickle
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class GetBrand(object):
    def __init__(self):
        self.url = r'http://qbt.ecdataway.com/brand'
        options = self.get_drvier_options
        self.brandriver = webdriver.Chrome(options=options)
        self.locator = (By.ID, 'header')
        self.month_lst = ['201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710','201711',
                          '201712', '201801', '201802', '201803', '201804', '201805', '201806', '201807',
                          '201808', '201809', '201810', '201811']
        self.datenum = datetime.now().strftime('%Y%m%d%H%M')

    @property
    def get_drvier_options(self):
        pref_chrome = {
            'profile.default_content_settings.popups': 0,
            'profile.default_content_settings.automaticDownloads': 0,
            "profile.managed_default_content_settings.images": 2,
            'download.default_directory': 'E:\\brand_down\\'}
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
        self.brandriver.implicitly_wait(10)
        if self.brandriver.find_elements_by_id('LoginForm_username'):
            self.brandriver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
            self.brandriver.implicitly_wait(10)
            self.brandriver.find_element_by_id('LoginForm_password').send_keys('a123')
            self.brandriver.find_element_by_class_name('login_btn').click()
        else:
            pass
        try:
            print('正在登录……')
            WebDriverWait(self.brandriver, 60).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
        except exceptions.TimeoutException as e:
            print(e)
            print('登录缓慢，请稍后……')
        return '登录成功！'

    def get_lst_of_brand(self):
        """根据指定的url选择所关注的20家品牌商的相关信息"""
        attribute = {}
        self.brandriver.get(self.url)
        try:
            WebDriverWait(self.brandriver, 60).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
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
        try:
            self.brandriver.get(brand_url)
            period_start = Select(self.brandriver.find_element_by_name('period'))
            period_start.select_by_value('201810')
            self.brandriver.find_element_by_id('submit-button').click()
        except exceptions.NoSuchElementException as e:
            self.login_qbt()
            self.sidebar_category(brand_url)
            print('4', e)
        try:
            WebDriverWait(self.brandriver, 30).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
        #     time.sleep(1)
        except exceptions.TimeoutException as e:
            self.login_qbt()
            self.sidebar_category(brand_url)
            print('2', e)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector('#sidebar_category > ul > li > a')
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
        # period_start = Select(self.brandriver.find_element_by_name('period'))
        #         # period_start.select_by_value('201810')
        #         # self.brandriver.find_element_by_id('submit-button').click()
        try:
            WebDriverWait(self.brandriver, 60).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
        #     time.sleep(1)
        except exceptions.TimeoutException as e:
            print('3', e)
            self.login_qbt()
            self.sidebar_category_second(midclss_url)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector('#sidebar_category > ul > li > a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'brand' in href:
                class_of_clothe[category.text] = href
        print('中类清单获取成功')
        return class_of_clothe

    def sidebar_element(self, clothe_url):
        """获取指定店铺的元素列表"""
        element_of_clothe = {}
        self.brandriver.get(clothe_url)
        try:
            WebDriverWait(self.brandriver, 60).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
            time.sleep(1)
        except exceptions.TimeoutException as e:
            print('3', e)
            self.login_qbt()
            self.sidebar_category_second(clothe_url)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector('#sidebar_category > ul > li > a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'cid' in href:
                element_of_clothe[category.text] = href
        print('元素清单获取成功')
        return element_of_clothe


    def get_link_excel(self):
        """通过三层访问，获取每一个品牌的链接、大类链接、中类链接和元素链接"""
        brand_df_concat = []
        all_brand_lst = self.get_lst_of_brand()
        for one_brand in all_brand_lst.items():
            brand_name, brand_url = one_brand
            one_brand_midclss = self.sidebar_category(brand_url).items()
            for one_midclss in one_brand_midclss:
                midclss, midclss_url = one_midclss
                clothe_clss = self.sidebar_category_second(midclss_url)
                # 获取一个品牌下的一个中类的链接清单
                for clothe in clothe_clss:
                    clothe_url = clothe_clss[clothe]
                    element_clss = self.sidebar_element(clothe_url)
                    if 'pos' in list(element_clss.values())[0]:
                        df_clothe_clss = pd.DataFrame(element_clss, index=['element_link']).transpose().reset_index()
                        df_clothe_clss['brand_name'] = brand_name
                        df_clothe_clss['brand_link'] = brand_url
                        df_clothe_clss['midclss'] = midclss
                        df_clothe_clss['midclss_url'] = midclss_url
                        df_clothe_clss['clothe'] = clothe
                        brand_df_concat.append(df_clothe_clss)
                    else:
                        clothe_clss_second = self.sidebar_category_second(clothe_url)
                        for clothe2 in clothe_clss_second:
                            clothe_url2 = clothe_clss_second[clothe2]
                            element_clss2 = self.sidebar_element(clothe_url2)
                            df_clothe_clss = pd.DataFrame(element_clss2, index=['element_link']).transpose().reset_index()
                            df_clothe_clss['brand_name'] = brand_name
                            df_clothe_clss['brand_link'] = brand_url
                            df_clothe_clss['midclss'] = midclss
                            df_clothe_clss['midclss_url'] = midclss_url
                            df_clothe_clss['clothe'] = clothe2
                            brand_df_concat.append(df_clothe_clss)
        brand_df = pd.concat(brand_df_concat, ignore_index=True)
        brand_df.to_excel('brand_link.xlsx')
        with open('brand2', 'wb') as f:
            f.write(pickle.dumps(brand_df))
        return 'all is ok'

    def get_one_category_detail(self, url_cagory):
        """通过url访问单个中类12个月的销售量信息"""
        url_trend = url_cagory + '&type=2#fold_line'
        # print(url_trend)
        self.brandriver.get(url_trend)
        try:
            WebDriverWait(self.brandriver, 30).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
            time.sleep(1)
            period_start = Select(self.brandriver.find_element_by_id('period_start'))
            period_start.select_by_value('201703')
            period_last = Select(self.brandriver.find_element_by_id('period_last'))
            period_last.select_by_value('201802')
            self.brandriver.find_element_by_css_selector('#f1 > table > tbody > tr:nth-child(6) > td:nth-child(2) > div > input[type="radio"]:nth-child(2)').click()
        except exceptions.TimeoutException as e:
            print('访问属性趋势', e)
            self.brandriver.refresh()
        except:
            self.login_qbt()
            self.get_one_category_detail(url_cagory)
        try:
            self.brandriver.find_element_by_id('submit-button').click()
            WebDriverWait(self.brandriver, 30).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(10)
            time.sleep(2)
        except exceptions.TimeoutException as e:
            print('访问属性趋势', e)
            self.brandriver.refresh()
        except:
            self.login_qbt()
            self.get_one_category_detail(url_cagory)
            time.sleep(3)
        return '文件检索成功'

    def got_file_from_web(self, brand_name, seniorclss, clothe_clss, eleclss):
        """将数据从网页上获取，处理成dataframe"""
        thead = self.brandriver.find_elements_by_css_selector('#content > div.charts > div > div.grid-view > table > thead')[0].text
        second_thead = thead.split('\n')[14:]
        second_thead.insert(0, '元素')
        tbody = self.brandriver.find_elements_by_css_selector('#content > div.charts > div > div.grid-view > table > tbody')[0]
        reptext = tbody.text.replace(', ', '&').split('\n')
        tbody_text = []
        for i in reptext:
            one_row = i.split(' ')
            a = len(one_row) - 25
            if a >= 1:
                one_row_s = one_row[a:]
            else:
                one_row_s = one_row
            tbody_text.append(one_row_s)
        one_table = pd.DataFrame(tbody_text, columns=second_thead)
        one_table.drop('涨幅', axis=1, inplace=True)
        one_table.columns = ['元素', '201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710', '201711',
                             '201712', '201801', '201802', '总计']
        one_table['brand_name'] = brand_name
        one_table['senior_clss'] = seniorclss
        one_table['clothe_clss'] = clothe_clss
        one_table['eleclss'] = eleclss
        one_table.to_excel('E:\\brand_down\\{0}_{1}_{2}_{3}.xls'.format(brand_name, seniorclss, clothe_clss.replace('/', '&'), eleclss))
        print('    {0}_{1}_{2}_{3}保存成功'.format(brand_name, seniorclss, clothe_clss.replace('/', '&'), eleclss))
        return one_table

    def main(self):
        with open('brand_2', 'rb') as f:
            df_brand = pickle.loads(f.read())
        print(self.login_qbt())
        for one_category in df_brand.values:
            clothe_clss = one_category[6].replace('/', '')
            brand_name = one_category[2].replace('/', '')
            seniorclss = one_category[4].replace('/', '')
            eleclss = one_category[0].replace('/', '')
            eleclss_url = one_category[1]
            print(brand_name, '正在访问------')
            print('    ', clothe_clss, eleclss, '正在下载')
            concat_df = pd.DataFrame()
            print(self.get_one_category_detail(eleclss_url))
            try:
                one_table = self.got_file_from_web(brand_name, seniorclss, clothe_clss, eleclss)
            except Exception as e:
                print(e)
                one_table = None
            concat_df = concat_df.append(one_table)
            concat_df.to_csv('./result/汇总_{}.csv'.format(self.datenum), mode='a', encoding='gbk')
            one_row = '    '.join([brand_name, clothe_clss, eleclss_url])
            with open("E:\\shop_url.txt", 'w', encoding='utf-8') as f:
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
