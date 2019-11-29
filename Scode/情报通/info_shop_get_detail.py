# coding: utf-8

"""
author: Aeenf
"""


import pathlib
import time
from urllib import parse

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class GetShop(object):
    def __init__(self):
        self.url = r'http://qbt.ecdataway.com/shop'
        options = self.get_drvier_options
        self.shopdriver = webdriver.Chrome(chrome_options=options)
        self.locator = (By.ID, 'header')

    @property
    def get_drvier_options(self):
        pref_chrome = {
            'profile.default_content_settings.popups': 0,
            'profile.default_content_settings.automaticDownloads': 0,
            'download.default_directory': 'I:\\SHOP中转\\'}
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_experimental_option('prefs', pref_chrome)
        options.add_extension(r"D:\Python\IPython\information\DogAuthExtension.crx")
        return options

    def login_qbt(self):
        """登录成功到情报通网站"""
        self.shopdriver.get(r'http://qbt.ecdataway.com/site/login')
        self.shopdriver.implicitly_wait(10)
        self.shopdriver.find_element_by_id('LoginForm_username').send_keys('森马上海服饰')
        self.shopdriver.implicitly_wait(10)
        self.shopdriver.find_element_by_id('LoginForm_password').send_keys('a123')
        self.shopdriver.find_element_by_class_name('login_btn').click()
        try:
            print('正在登录……')
            WebDriverWait(self.shopdriver, 60).until(EC.presence_of_element_located(self.locator))
            self.shopdriver.implicitly_wait(20)
        except exceptions.TimeoutException as e:
            print(e)
            print('登录缓慢，请稍后……')
        return '登录成功！'

    def get_lst_of_shop(self):
        """根据指定的url选择所关注的20家品牌商的相关信息"""
        attribute = {}
        self.shopdriver.get(self.url)
        try:
            WebDriverWait(self.shopdriver, 60).until(EC.presence_of_element_located(self.locator))
            self.shopdriver.implicitly_wait(10)
        #     time.sleep(10)
        except Exception as e:
            print('1', e)
        all_href = self.shopdriver.find_elements_by_css_selector('a')
        for link in all_href:
            try:
                href = link.get_attribute('href')
                if 'index?sid=' in href:
                    name = parse.unquote(href).split('=')[2]
                    attribute[name] = href
            except TypeError as e:
                pass
        print('店铺列表和链接获取成功')
        return attribute

    def sidebar_category(self, shop_url):
        """获取指定店铺的中类列表"""
        class_of_clothe = {}
        self.shopdriver.get(shop_url)
        try:
            WebDriverWait(self.shopdriver, 60).until(EC.presence_of_element_located(self.locator))
            self.shopdriver.implicitly_wait(10)
        #     time.sleep(1)
        except exceptions.TimeoutException as e:
            print('2', e)
        all_sidebar_category = self.shopdriver.find_elements_by_css_selector('a')
        for category in all_sidebar_category:
            href = category.get_attribute('href')
            if 'index?cid=' in href:
                class_of_clothe[category.text] = href
        print('中类清单获取成功')
        return class_of_clothe

    def get_one_category_detail(self, url_cagory):
        """通过url访问单个中类的销售额"""
        js = 'document.getElementById(\'is_price\').value=1;document.getElementById(\'is_csv\').value=1;document.f1.submit();'
        locator_set1 = (By.ID, 'set1')
        url_trend = url_cagory + '&type=2#fold_line'
    # list(class_of_clothe.values())
        self.shopdriver.get(url_trend)
        try:
            WebDriverWait(self.shopdriver, 60).until(EC.presence_of_element_located(locator_set1))
            self.shopdriver.implicitly_wait(10)
            time.sleep(1)
        except exceptions.TimeoutException as e:
            print('3', e)
            self.shopdriver.refresh()
            time.sleep(5)
        period_start = Select(self.shopdriver.find_element_by_id('period_start'))
        period_start.select_by_value('201707')
        period_last = Select(self.shopdriver.find_element_by_id('period_last'))
        period_last.select_by_value('201712')
        self.shopdriver.find_element_by_css_selector('#show_line_date').click()
        self.shopdriver.find_element_by_css_selector('#f1 > table > tbody > tr:nth-child(6) > td:nth-child(2) > input:nth-child(2)').click()
        self.shopdriver.find_element_by_id('submit-button').click()
        try:
            time.sleep(5)
            WebDriverWait(self.shopdriver, 60).until(EC.presence_of_element_located(locator_set1))
            self.shopdriver.implicitly_wait(10)
        except exceptions.TimeoutException as e:
            print('4', e)
            self.shopdriver.refresh()
            time.sleep(5)
        self.shopdriver.execute_script(js)
        time.sleep(5)
        return '     文件下载成功'

    def rename_xls(self, shop, category):
        p = pathlib.Path(r'I:\SHOP中转')
        try:
        	down_file = [i for i in p.iterdir()][0]
        # print(down_file.name, '已经存储在I盘')
        	new_name = 'I:\\情报通shop\\{0}_{1}.xls'.format(shop, category.replace('/', '&'))
        	down_file.rename(new_name)
        except Exception as e:
        	pass
        s = '     ' + shop + ' ' + category + ' 重命名成功\n'
        return s

    def main(self):
        print(self.login_qbt())
        time.sleep(5)
        shop_attribute = self.get_lst_of_shop()
        shop_attribute.pop('茵曼旗舰店')
        for shop in shop_attribute.keys():
            shop_url = shop_attribute[shop]
            print(shop, '正在访问------')
            all_sidebar_category = self.sidebar_category(shop_url)
            for one_category in all_sidebar_category.keys():
                print('    ', one_category, '正在下载')
                url_category = all_sidebar_category[one_category]
                print(self.get_one_category_detail(url_category))
                time.sleep(10)
                print(self.rename_xls(shop, one_category))
                time.sleep(4)
                one_row = '    '.join([shop, one_category, url_category])
                with open('i:shop_url.txt', 'a', encoding='utf-8') as f:
                	f.write(one_row)
                	f.write('\n')
                continue
        print('所有的店铺均已完成')
        self.shopdriver.quit()
        return '运行结束'


if __name__ == "__main__":
    shop_detail = GetShop()
    print(shop_detail.main())






# table_text = self.shopdriver.find_element_by_id('set1').text
# table_text.split('\n')
# s = []
# for y in [i.split(' ') for i in table_text.split('\n')]:
#     for x in y:
#         s.append(x)
# s = s[20:]
# df = pd.DataFrame([s[i: i+13] for i in range(0, len(s), 13)])
# df['店铺'] = item_name
# df.to_excel('i:{}.xls'.format(item_name), index=False, encoding='utf-8', header=False)

        # locator_set1 = (By.ID, 'set1')


