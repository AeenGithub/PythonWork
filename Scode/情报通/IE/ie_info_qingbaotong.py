# coding: utf-8

"""
author：Aeenf
"""

import pathlib
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class GetFile(object):
    def __init__(self, files):
        self.file = files
        self.locator = (By.ID, 'header')
        self.url_lst = self.get_one_url()
        self.driver = webdriver.Ie()
        # self.dic_name = self.get_name_from_csv()

    def get_one_url(self):
        """从文件获取需要爬取的url链接"""
        with open(self.file, 'r', encoding='utf-8') as f:
            for one_url in f.readlines():
                yield one_url

    @property
    def login(self):
        """登录成功到情报通网站"""
        '''选中服装鞋包页面主页'''
        self.driver.get(r'http://qbt.ecdataway.com/site/login')
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_id('LoginForm_username').clear()
        self.driver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
        # self.driver.implicitly_wait(1)
        self.driver.find_element_by_id('LoginForm_password').send_keys('a123')
        self.driver.find_element_by_class_name('login_btn').click()
        try:
            print('正在登录……')
            WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.locator))
            self.driver.implicitly_wait(2)
        except exceptions.TimeoutException as e:
            print(e)
            self.driver.refresh()
            print('登录缓慢，正在刷新，请稍后……')
            self.login()
            time.sleep(5)
        print('登录成功！')
        # self.driver.get(r'http://qbt.ecdataway.com/stat#fold_line')
        # try:
        #     WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))
        #     self.driver.implicitly_wait(5)
        #     self.driver.find_element_by_css_selector('#sidebar_category > ul > li:nth-child(4) > a').click()
        # except:
        #     print('time is short and  need take long time')
        return '首页访问成功并且已经进入服装鞋包界面'

    def click_button(self, url):
        """
        :param url: url
        :return: 根据指定的url选择属性趋势、天猫、时间段和数据表等选项
        """
        locator_set1 = (By.ID, 'set1')
        js = '''document.getElementById('is_price').value=1;document.getElementById('is_csv').value=1;document.f1.submit();'''
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.locator))
            self.driver.implicitly_wait(6)
            time.sleep(5)
        except Exception as e:
            print('1', e)
            self.driver.refresh()
            print('主页访问失败，正在刷新，请稍后……')
            time.sleep(1)
        self.driver.find_element_by_css_selector(
            '#content > div.charts > div > div.submenu > a:nth-child(2) > span.body').click()
        try:
            WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.locator))
            self.driver.implicitly_wait(3)
            time.sleep(1)
        except exceptions.TimeoutException as e:
            print('2', e)
            self.driver.refresh()
            print('属性趋势失败，正在刷新，请稍后……')
            time.sleep(1)
        period_start = Select(self.driver.find_element_by_id('period_start'))
        period_start.select_by_value('201707')
        period_last = Select(self.driver.find_element_by_id('period_last'))
        period_last.select_by_value('201712')
        self.driver.find_element_by_name('is_mall').click()
        # '#f1 > table > tbody > tr:nth-child(6) > td:nth-child(2) > input:nth-child(1)'
        self.driver.find_element_by_css_selector(
            '#f1 > table > tbody > tr:nth-child(6) > td:nth-child(2) > input:nth-child(1)').click()
        self.driver.find_element_by_id('submit-button').click()
        try:
            WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(locator_set1))
            self.driver.implicitly_wait(3)
            time.sleep(2)
        except exceptions.TimeoutException as e:
            print('3', e)
            self.driver.refresh()
            print('检索失败，正在刷新，请稍后……')
            time.sleep(1)
        # self.driver.find_element_by_css_selector('#content > div.charts > div > div.padding-15 > p > button').click()
        try:
            self.driver.execute_script(js)
            self.driver.implicitly_wait(3)
            time.sleep(2)
            return '     下载成功到E盘-情报通文件'
        except exceptions.TimeoutException as e:
            print('4', e)
            self.driver.refresh()
            time.sleep(2)
            return url, '下载失败，请重新调用\n'

    def get_name_from_csv(self):
        """获取连接和对应文件名"""
        dic = {}
        with open(self.file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url = i.split(',')[0].strip('\n')
                name = i.split(',')[1].strip('\n')
                dic[url] = name
        return dic

    def rename_xls(self, url):
        p = pathlib.Path(r'E:\中转')
        try:
            down_file = [i for i in p.iterdir()][0]
        except IndexError as e:
            print(e, '-----数据下载失败， 正在刷新----')
            self.driver.refresh()
            time.sleep(10)
        # print(down_file.name, '已经存储在E盘')
            down_file = [i for i in p.iterdir()][0]
        print('    ',self.dic_name[url], '重命名成功\n')
        new_name = 'E:\\情报通文件\\' + self.dic_name[url] + '.xls'
        down_file.rename(new_name)
        time.sleep(3)
        return '\n'

    @property
    def main(self):
        """主函数，运行所有功能"""
        print(self.login)
        with open(self.file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url_init = i.split(',')[0]
                print('休闲裤', i.split(',')[1].strip('\n'), '正在访问')
                url = 'http://' + url_init + '#fold_line'
                # print(url)
                try:
                    print(self.click_button(url))
                except Exception as e:
                    print('all',e)
                    print(self.login)
                    print(self.click_button(url))
                print(self.rename_xls(url_init))
                time.sleep(10)
                continue
        self.driver.quit()
        return '所有的都已经运行结束'


if __name__ == '__main__':
    file = r"D:\Python\QinBaot\test.csv"
    get_file = GetFile(file)
    print(get_file.login)
