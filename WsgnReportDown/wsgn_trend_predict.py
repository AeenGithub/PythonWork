# -*-coding:utf-8-*-
__author__ = 'AeenPython'

import json
import os
import random
import re
import time

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TrenePredictReport(object):
    def __init__(self):
        # 添加wsgn登陆网址
        self.wsgn_url = r'https://www.wgsnchina.cn/cs/login/?r=/home/'
        self.file_save_dir = 'E:\\WsgnReport\\'
        options = self.get_drvier_options
        self.locator = (By.ID, 'login-email-user')
        # 对chrome进行各项配置
        self.wsgndriver = webdriver.Chrome(options=options)

    @property
    def get_drvier_options(self):
        pref_chrome = {
            'profile.default_content_settings.popups': 0,
            # 设置chrome不显示受控制
            'profile.default_content_settings.automaticDownloads': 0,
            # 设置chrome不显示图片
            "profile.managed_default_content_settings.images": 2,
            # 设置chrome的默认下载位置
            'download.default_directory': self.file_save_dir
        }
        options = webdriver.ChromeOptions()
        # 设置chrome不显示受控制
        options.add_argument('disable-infobars')
        options.add_argument('lang=zh_CN.UTF-8')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('prefs', pref_chrome)
        return options

    def downloaded_file_name(self):
        # last_file_dir = r'D:\内部共享\WSGN报告\20190705'
        file_lst = os.listdir(self.file_save_dir)
        # file_lst = os.listdir(last_file_dir)
        all_file = [''.join(re.findall('([\u4e00-\u9fa5]{1,})', i)) for i in file_lst]
        return all_file

    def wsgn_sign_in(self):
        try:
            self.wsgndriver.get(self.wsgn_url)
            time.sleep(1)
            self.wsgndriver.implicitly_wait(100)
            # WebDriverWait(self.wsgndriver, 1).until(EC.presence_of_element_located(self.locator))
            # self.wsgndriver.implicitly_wait(1)
            print('WSGN CHINA 正在登陆')
            self.wsgndriver.find_element_by_id('login-email-user').clear()
            self.wsgndriver.find_element_by_id('login-email-user').send_keys('masijing@semir.com')
            self.wsgndriver.find_element_by_id('login-password').clear()
            self.wsgndriver.find_element_by_id('login-password').send_keys('MASIJING1234')
            # self.wsgndriver.implicitly_wait(3)
            time.sleep(0.2)
            self.wsgndriver.find_element_by_id('login-submit-button').click()
            print('WSGN CHINA 登陆成功')
            time.sleep(0.1)
            self.wsgndriver.implicitly_wait(5)
        except exceptions.TimeoutException as e:
            print(e)
            print('登录超时，重新登录')
            self.wsgndriver.refresh()
            self.wsgn_sign_in()
        except Exception as e:
            print(e)

    def get_page_source(self, page):
        size = 24
        querying_json = {'from': page * size,
                         'size': size,
                         'sort': 'date',
                         'products': [4822],
                         'filters': {
                             'seasons': ['2431']
                         }}
        querying = json.dumps(querying_json)
        part_url = '''https://www.wgsnchina.cn/api/beet/content/search?q={}'''.format(querying)
        self.wsgndriver.get(part_url)
        time.sleep(random.random() * 5)
        page_source = self.wsgndriver.page_source
        return page_source

    def get_total_url(self):
        total_pages_article = []
        page = 0
        page_source = self.get_page_source(page)
        page_json = json.loads(re.findall('{.*}', page_source)[0])
        total_articles = int(page_json['total'])
        total_pages = total_articles // 24 + 1
        for one_page in range(total_pages):
            print('\t第 {} 页链接正在获取中'.format(one_page + 1))
            page_source = self.get_page_source(one_page)
            page_json = json.loads(re.findall('{.*}', page_source)[0])
            content = page_json['content']
            for one_pieces in content:
                authors = one_pieces.get('authors')
                if authors:
                    authors = authors[0]
                else:
                    authors = ''
                blurb = one_pieces.get('blurb')
                date = one_pieces.get('date')
                article_id = one_pieces.get('id')
                images = one_pieces.get('images')
                if images:
                    images = images.get('carousel')
                else:
                    images = ''
                seasons = one_pieces.get('labels').get('seasons')
                if seasons:
                    seasons = seasons[0].get('name')
                else:
                    seasons = ''
                page_number = one_pieces.get('page_number')
                title = one_pieces.get('title')
                one_article = (
                    authors,
                    blurb,
                    date,
                    article_id,
                    images,
                    seasons,
                    page_number,
                    title
                )
                total_pages_article.append(one_article)
            print('\t第 {} 页链接下载完毕\n'.format(one_page + 1))
        article_pages_df = pd.DataFrame(total_pages_article)
        article_pages_df.columns = [
            'authors',
            'blurb',
            'date',
            'article_id',
            'images',
            'seasons',
            'page_number',
            'title'
        ]
        article_pages_df.to_pickle('../WsgnReportDown/Pickle/total_url.pickle')
        print('所有的链接已经保存陈功')
        return article_pages_df

    def download_each_report(self, article_id):
        download_svg = (By.CSS_SELECTOR, '#wrap')
        article_url = r'https://www.wgsnchina.cn/content/board_viewer/#/{}/page/1'.format(article_id)
        self.wsgndriver.get(article_url)
        time.sleep(4)
        WebDriverWait(self.wsgndriver, 10).until(EC.presence_of_element_located(download_svg))
        self.wsgndriver.implicitly_wait(10)
        self.wsgndriver.find_element_by_css_selector('#toolbar > div.tool.btn-download').click()
        time.sleep(4)
        print('\t下载完成，正在保存\n')

    def main(self):
        report_down.wsgn_sign_in()
        # article_pages_df = self.get_total_url()
        article_pages_df = pd.read_pickle('../WsgnReportDown/Pickle/total_url.pickle')
        total_counts = article_pages_df.shape[0]
        count = 1
        article_dict = list(article_pages_df.T.to_dict().values())
        for each_article_dict in article_dict:
            article_id = each_article_dict['article_id']
            title = each_article_dict['title']
            file_name = ''.join(re.findall('([\u4e00-\u9fa5]{1,})', title))
            if file_name in self.downloaded_file_name():
                print('一共有{}篇文章, 第 {} 篇 《{}》 已经完成'.format(total_counts, count, title))
            else:
                print('一共有{}篇文章, 第 {} 篇 《{}》 正在下载中'.format(total_counts, count, title))
                try:
                    self.download_each_report(article_id)
                except exceptions.NoSuchElementException as e:
                    print(e)
                    pass
                except exceptions.NoSuchWindowException as e:
                    break
                except exceptions.WebDriverException as e:
                    break
            count += 1
        self.wsgndriver.quit()


if __name__ == '__main__':
    report_down = TrenePredictReport()
    report_down.main()
    # report_down.wsgn_sign_in()