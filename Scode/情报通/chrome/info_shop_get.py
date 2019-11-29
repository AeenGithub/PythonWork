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
from selenium.webdriver.support.ui import WebDriverWait


class GetFile(object):
    def __init__(self, files):
        self.file = files
        self.locator = (By.ID, 'header')
        self.url_lst = self.get_one_url()
        pref_chrome = {
            'profile.default_content_settings.popups': 0,
            'profile.default_content_settings.automaticDownloads': 0,
            'download.default_directory': 'I:\\中转\\'
        }
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_experimental_option('prefs', pref_chrome)
        options.add_extension(r"D:\Python\IPython\information\DogAuthExtension.crx")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.dic_name = self.get_name_from_csv()

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
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('LoginForm_password').send_keys('a123')
        self.driver.find_element_by_class_name('login_btn').click()
        try:
            print('正在登录……')
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(self.locator))
            self.driver.implicitly_wait(20)
        except exceptions.TimeoutException as e:
            print(e.filename)
            print('登录缓慢，请稍后……')
        print('登录成功！')
        # self.driver.get(r'http://qbt.ecdataway.com/stat#fold_line')
        # try:
        #     WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))
        #     self.driver.implicitly_wait(5)
        #     self.driver.find_element_by_css_selector('#sidebar_category > ul > li:nth-child(4) > a').click()
        # except:
        #     print('time is short and  need take long time')
        return '首页访问成功并且已经进入服装鞋包界面'

    def click_button(self):
        url = r'http://qbt.ecdataway.com/shop'
        """
        :param url: url
        :return: 根据指定的url选择所关注的20家品牌商的相关信息
        """
        # locator_set1 = (By.ID, 'set1')
        js = '''document.getElementById('is_price').value=1;document.getElementById('is_csv').value=1;document.f1.submit();'''
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(self.locator))
            self.driver.implicitly_wait(60)
            time.sleep(10)
        except Exception as e:
            print('1', e)
            return '主页访问失败，需要更久的时间'
        self.driver.find_element_by_css_selector('#tag-flag > tr:nth-child(1) > td:nth-child(1) > a').text
        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(self.locator))
            self.driver.implicitly_wait(30)
            time.sleep(1)
        except exceptions.TimeoutException as e:
            print('2', e)
            print('店铺列表访问失败，需要更久的时间')
        # period_start = Select(self.driver.find_element_by_id('period_start'))
        # period_start.select_by_value('201707')
        # period_last = Select(self.driver.find_element_by_id('period_last'))
        # period_last.select_by_value('201712')
        # self.driver.find_element_by_name('is_mall').click()
        # self.driver.find_element_by_css_selector(
        #     '#f1 > table > tbody > tr:nth-child(6) > td:nth-child(2) > input:nth-child(2)').click()
        # self.driver.find_element_by_id('submit-button').click()
        # try:
        #     WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(locator_set1))
        #     self.driver.implicitly_wait(30)
        #     time.sleep(1)
        # except exceptions.TimeoutException as e:
        #     print('3', e)
        #     print('check failed and need take long time')
        # # self.driver.find_element_by_css_selector('#content > div.charts > div > div.padding-15 > p > button').click()
        # try:
        #     self.driver.execute_script(js)
        #     self.driver.implicitly_wait(30)
        #     time.sleep(2)
        #     return url, '下载成功到-/I盘/情报通文件/-\n'
        # except exceptions.TimeoutException as e:
        #     print('4', e)
        #     return url, '下载失败，请重新调用\n'

    def get_name_from_csv(self):
        """获取连接和对应文件名"""
        dic = {}
        with open(self.file, 'r') as f:
            for i in f.readlines():
                url = i.split(',')[0]
                name = i.split(',')[1].strip('\n')
                dic[url] = name
        return dic

    def rename_xls(self, url):
        p = pathlib.Path(r'I:\中转')
        down_file = [i for i in p.iterdir()][0]
        print(down_file.name, '已经存储在I盘')
        print(self.dic_name[url], '下载成功')
        new_name = 'I:\\情报通文件\\' + self.dic_name[url] + '.xls'
        down_file.rename(new_name)
        return '重命名成功'

    @property
    def main(self):
        """主函数，运行所有功能"""
        # print(self.login)
        time.sleep(5)
        print(self.click_button())
        time.sleep(5)
        return '所有的都已经运行结束'


if __name__ == '__main__':
    file = r"I:\\URLNAME.csv"
    get_file = GetFile(file)
    print(get_file.main)
