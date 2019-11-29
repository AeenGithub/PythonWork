# -*_coding:utf-8-*-

import random
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class taobao_use_firefox(object):
    def __init__(self):
        self.url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.3538.102 Safari/537.36'
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", user_agent)
        fp.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.username = '17621780176'
        self.password = "www.,194928.,com"
        self.nickname = '风云决地起'

    def set_initi_navigator(self):
        self.driver.execute_script('''Object.defineProperties(navigator,{webdriver:{get:() => undefined}})''')
        self.driver.execute_script('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        self.driver.execute_script('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        self.driver.execute_script('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    def silde_login_code(self):
        slide_code = self.driver.find_elements_by_css_selector('#nc_1_wrapper')
        print('出现滑块错误')
        if slide_code:
            action = ActionChains(self.driver)
            source = self.driver.find_element_by_xpath("//*[@id='nc_1_n1t']/span")  # 需要滑动的元素
            action.click_and_hold(source).perform()
            time.sleep(0.5)
            action.move_by_offset(258, 0)  # 需要滑动的坐标
            time.sleep(1)
            action.release().perform()  # 释放鼠标
            print('滑块解锁完成')


    def login_taobao(self):
        def input_name_password():
            login_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
            login_element.click()
            useranme = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1')))
            useranme.clear()
            for i in self.username:
                useranme.send_keys(i)
                time.sleep(random.random()/4)
            # username_js = '''document.getElementById("TPL_username_1").value="{}"'''.format(self.username)
            # self.driver.execute_script(username_js)
            time.sleep(1.2)
            sina_password = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_password_1')))
            sina_password.clear()
            for i in self.password:
                sina_password.send_keys(i)
                time.sleep(random.random()/4)
        self.driver.get(self.url)
        self.set_initi_navigator()
        time.sleep(random.random()*5)
        input_name_password()
        submit = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_SubmitStatic')))
        submit.click()
        try:
            site_user = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'site-nav-user')))
            if site_user:
                if site_user.text.split('\n')[0] == self.nickname:
                    print('登陆成功到淘宝网')
                    # print(self.driver.get_cookies())
                else:
                    print('找不到昵称， 登陆失败，请重新登陆')
                    input_name_password()
                    self.silde_login_code()
        except exceptions.NoSuchElementException as e:
            print('没有定位到昵称元素，登陆失败')
            input_name_password()
            self.silde_login_code()


if __name__ == '__main__':
    taobao_firefox = taobao_use_firefox()
    taobao_firefox.login_taobao()


# wrong_password = self.driver.find_elements_by_css_selector('html.ks-webkit537.ks-webkit.ks-chrome44.ks-chrome body.chl-reg div#page div#content div.content-layout div.login-box-warp div#J_LoginBox.login-box.no-longlogin.module-static div.bd div#J_StaticForm.static-form form#J_Form div#J_Message.login-msg.error p.error')