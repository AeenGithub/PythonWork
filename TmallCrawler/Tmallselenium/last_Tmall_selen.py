
import random
import time

from selenium import webdriver
from selenium.webdriver import ActionChains


class TmallSenl(object):
    def __init__(self):
        user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/630.0.3538.77 Safari/537.36'
        ]
        self.headers = random.choice(user_agent)
        fp = webdriver.FirefoxProfile()
        fp.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile=fp)

    def script_exec(self):
        script_webdriver = '''Object.defineProperties(navigator,{
        webdriver:{
        get:() => false
        }
        })'''
        script_language = ''' Object.defineProperty(navigator, 'languages', {
            get: () => ["zh-CN", "zh", "en-US", "en"],
          });'''
        self.driver.execute_script(script_webdriver)
        self.driver.execute_script(script_language)

    def tmall_login(self):
        self.driver.get('https://semir.m.tmall.com/shop/shop_auction_search.htm?sort=default')
        iframe = self.driver.find_element_by_css_selector('#sufei-dialog-content')
        self.driver.switch_to.frame(iframe)
        self.driver.find_element_by_css_selector('#TPL_username_1').send_keys('17621780176')
        self.driver.find_element_by_css_selector('#TPL_password_1').send_keys('www.,194928.,com')
        self.driver.find_element_by_css_selector('#J_SubmitStatic').click()
        self.driver.find_element_by_css_selector('#TPL_password_1').send_keys('www.,194928.,com')
        time.sleep(10)
        action = ActionChains(self.driver)
        source = self.driver.find_element_by_xpath("//*[@id='nc_1_n1t']/span")  # 需要滑动的元素
        action.click_and_hold(source).perform()
        time.sleep(0.5)
        action.move_by_offset(206, 0)  # 需要滑动的坐标
        time.sleep(1.2)
        action.release().perform()  # 释放鼠标
        self.driver.find_element_by_css_selector('#J_SubmitStatic').click()

    def outside_code(self):
        try:
            iframe = self.driver.find_element_by_css_selector('#sufei-dialog-content')
            self.driver.switch_to.frame(iframe)
        except:
            print('no need switch to iframe')
        try:
            action = ActionChains(self.driver)
            source = self.driver.find_element_by_xpath("//*[@id='nc_1_n1t']/span")  # 需要滑动的元素
            action.click_and_hold(source).perform()
            time.sleep(0.5)
            action.move_by_offset(265, 0)  # 需要滑动的坐标
            time.sleep(1.2)
            action.release().perform()  # 释放鼠标
        except:
            pass
        return '滑动解锁完成'

    def main(self):
        self.script_exec()
        self.tmall_login()

if __name__ == '__main__':
    tmall = TmallSenl()
    print(tmall.main())