# coding: utf-8

"""
author: Aeenf
"""


import logging
import pickle

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
        self.brandriver = webdriver.Chrome(chrome_options=options)
        self.locator = (By.ID, 'header')
        self.init_class = {
            '女装女士精品 ': 'http://qbt.ecdataway.com/stat?rcid=2011010114&cid=16#fold_line',
            '男装': 'http://qbt.ecdataway.com/stat?rcid=2011010114&cid=30#fold_line',
            '内衣家居服': 'http://qbt.ecdataway.com/stat?rcid=2011010114&cid=1625#fold_line',
        }

    def getlog(self):
        '''通过使用logging包将程序运行出错的地方进行记录'''
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='D:\\爬虫日志\\Tmall_detail_get.log',
                            filemode='a')
    @property
    def get_drvier_options(self):
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

    def login_qbt(self):
        """登录成功到情报通网站"""
        try:
            print('正在登录……')
            self.brandriver.get(r'http://qbt.ecdataway.com/site/login')
            self.brandriver.implicitly_wait(1)
            self.brandriver.find_element_by_id('LoginForm_username').clear()
            self.brandriver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
            self.brandriver.implicitly_wait(1)
            self.brandriver.find_element_by_id('LoginForm_password').send_keys('a123')
            self.brandriver.find_element_by_class_name('login_btn').click()
            WebDriverWait(self.brandriver, 10).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(5)
        # except exceptions.TimeoutException as e:
        #     print(e)
        #     print('登录缓慢，请稍后……')
        except Exception:
            print('登录异常，重新登录')
            self.login_qbt()
        return '登录成功！'

    def sidebar_category(self, senior_url):
        """获取侧边栏的中类列表"""
        class_of_sexandboy = {}
        self.brandriver.get(senior_url)
        try:
            WebDriverWait(self.brandriver, 6).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(1)
        except exceptions.TimeoutException as e:
            self.login_qbt()
            self.sidebar_category(senior_url)
            print('2', e)
        all_sidebar_category = self.brandriver.find_elements_by_css_selector(
            '#sidebar_category > ul > li > a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'rcid' in href:
                class_of_sexandboy[category.text] = href
        print('中类清单获取成功')
        return class_of_sexandboy

    def sidebar_category_second(self, midclss_url):
        """获取侧边栏的元素列表"""
        class_of_clothe = {}
        self.brandriver.get(midclss_url)
        try:
            WebDriverWait(self.brandriver, 6).until(
                EC.presence_of_element_located(self.locator))
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
            if 'pos' in href:
                class_of_clothe[category.text] = href
        print('元素清单获取成功')
        return class_of_clothe

    def get_link_excel(self):
        """通过三层访问，获取每一个大类、中类和元素链接"""
        brand_df_concat = []
        all_senior_lst = self.init_class
        for one_senior in all_senior_lst.items():
            seniorclss_name, senior_url = one_senior
            all_midclss = self.sidebar_category(senior_url).items()
            for one_midclss in all_midclss:
                one_clss, one_url = one_midclss
                ele_clss = self.sidebar_category_second(one_url)
                # 获取一个中类下的一个大类的链接清单
                df_ele_clss = pd.DataFrame(
                    ele_clss, index=['clothe_link']).transpose().reset_index()
                df_ele_clss['seniorclss'] = seniorclss_name
                df_ele_clss['senior_url'] = senior_url
                df_ele_clss['midclss'] = one_clss
                df_ele_clss['midclss_url'] = one_url
                brand_df_concat.append(df_ele_clss)
        brand_df = pd.concat(brand_df_concat, ignore_index=True)
        brand_df.to_excel('./情报通/IE/seniorclss_link.xlsx')
        with open('./情报通/IE/brand', 'wb') as f:
            f.write(pickle.dumps(brand_df))
        return df_ele_clss

    def click_button(self, url):
        """根据指定的url选择属性趋势、天猫、时间段和数据表等选项"""
        try:
            self.brandriver.get(url)
            WebDriverWait(self.brandriver, 6).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(6)
        # except exceptions.TimeoutException as e:
        #     print('1\tclick button', e, '\n主页访问失败，正在刷新，请稍后……')
        #     self.brandriver.refresh()
        # except Exception:
        #     self.login_qbt()
        #     self.click_button(url)
        # try:
            self.brandriver.find_element_by_css_selector('#content > div.charts > div > div.submenu > a:nth-child(2) > span.body').click()
            WebDriverWait(self.brandriver, 6).until(
                EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(3)
            period_start = Select(
                self.brandriver.find_element_by_id('period_start'))
            period_start.select_by_value('201803')
            period_last = Select(
                self.brandriver.find_element_by_id('period_last'))
            period_last.select_by_value('201809')
            self.brandriver.find_element_by_name('is_mall').click()
            self.brandriver.find_element_by_css_selector(
                '#f1 > table > tbody > tr:nth-child(6) > td:nth-child(2) > input:nth-child(1)').click()
        # except exceptions.TimeoutException as e:
        #     self.brandriver.refresh()
        #     print('主页访问失败，正在刷新，请稍后……')
        # except Exception:
        #     self.login_qbt()
        #     self.click_button(url)
        # try:
            self.brandriver.find_element_by_id('submit-button').click()
            WebDriverWait(self.brandriver, 20).until(EC.presence_of_element_located(self.locator))
            self.brandriver.implicitly_wait(3)
        # except exceptions.TimeoutException as e:
        #     self.brandriver.refresh()
        #     print('主页访问失败，正在刷新，请稍后……')
        except Exception:
            self.login_qbt()
            self.click_button(url)
        return '\t\t检索成功'

    def got_file_from_web(self, senior_clss, ele_clss, midclss):
        """将数据从网页上获取，处理成dataframe"""
        def func(x):
            '''利用map函数进行规整数据'''
            one = x.split(' ')
            a = len(one) - longt
            fir = [''.join(one[:a+1])]
            fir.extend(one[a+1:])
            return fir
        thead1 = self.brandriver.find_elements_by_css_selector('#set1 > thead > tr')[1].text
        thead0 = self.brandriver.find_elements_by_css_selector('#set1 > thead > tr')[0].text
        tbody = self.brandriver.find_elements_by_css_selector('#set1 > tbody')[0].text
        longt = len(thead0.split('\n')[2:-1]) * 2 + 3
        df_tbody = pd.DataFrame(list(map(func, tbody.split('\n'))))
        df_tbody.set_index(0, drop=True, inplace=True)
        df_tbody.columns = thead1.split('\n')
        df_tbody.drop(['环比'], axis=1, inplace=True)
        df_tbody.columns = df_tbody.columns + thead0.split('\n')[1:]
        df_tbody['senior_clss'] = senior_clss
        df_tbody['midclss'] = midclss
        df_tbody['ele_clss'] = ele_clss
        df_tbody.to_excel('D:\\QinBaot_ele\\{0}_{1}_{2}.xls'.format(
            senior_clss, midclss, ele_clss))
        print('{0}_{1}_{2}保存成功'.format(senior_clss, midclss, ele_clss))
        return df_tbody

    def main(self):
        with open('./情报通/IE/brand', 'rb') as f:
            df_brand = pickle.loads(f.read())
        print(self.login_qbt())
        concat_df = pd.DataFrame()
        for i in range(df_brand.shape[0]):
            ele_clss = df_brand.loc[i, 'index'].replace('/', '')
            ele_url = df_brand.loc[i, 'clothe_link']
            senior_clss = df_brand.loc[i, 'seniorclss']
            midclss = df_brand.loc[i, 'midclss'].replace('/', '')
            print(senior_clss, '正在访问------')
            print('\t\t{}正在下载'.format(ele_clss))
            print(self.click_button(ele_url))
            try:
                one_month_table = self.got_file_from_web(senior_clss, ele_clss, midclss)
            except Exception as e:
                print(e, '\n文件检索成功，下载失败')
                logging.info('{0}_{1}_{2}保存成功'.format(senior_clss, midclss, ele_clss))
                one_month_table = pd.DataFrame()
            concat_df = concat_df.append(one_month_table)
            one_month_table.to_csv('./情报通/result/ele_gather.csv', mode='a', encoding='gbk')
            with open('./情报通/result/ele_gather', mode='wb') as f:
                f.write(pickle.dumps(concat_df))
            df_brand.loc[i+1:].to_csv('./情报通/result/residue.csv', encoding='gbk')
            continue
        print('所有的中类均已完成')
        self.brandriver.quit()
        return '运行结束'


if __name__ == "__main__":
    brand_detail = GetBrand()
    # print(brand_detail.main())
    print(brand_detail.login_qbt())
    print(brand_detail.get_link_excel())
