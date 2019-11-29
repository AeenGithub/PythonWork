import json
import random
import re
import time

import pandas as pd
from selenium.webdriver import ActionChains


# iframe2 = driver.find_element_by_css_selector('#sufei-dialog-content')
def outside_code():
    try:
        iframe = driver.find_element_by_css_selector('#sufei-dialog-content')
        driver.switch_to.frame(iframe)
    except:
        print('no need switch to iframe')
    try:
        action = ActionChains(driver)
        source=driver.find_element_by_xpath("//*[@id='nc_1_n1t']/span")#需要滑动的元素
        action.click_and_hold(source).perform()
        time.sleep(0.5)
        action.move_by_offset(260,0) #需要滑动的坐标
        time.sleep(random.random())
        action.release().perform()  #释放鼠标
    except IndexError:
        pass
    return '滑动解锁完成'

def func_totalpage():
    firt_page_url = 'https://{}.m.tmall.com/shop/shop_auction_search.do?ajson=1&_tm_source=tmallsearch&sort=s&p=1&page_size=12&from=h5&shop_id=57303596&callback=jsonp_{}'.format(shop_name, num)
    driver.get(firt_page_url)
    html = driver.page_source
    try:
        infos = re.findall(r'\(({.*})\)', html)[0]
        infos = json.loads(infos)
        totalpage = int(infos.get('total_page'))
        return int(totalpage*1.04)
    except IndexError:
        raise IndexError

def get_totalpage():
    try:
        totalpage = func_totalpage()
    except IndexError:
        driver.get('https://{}.m.tmall.com/shop/shop_auction_search.htm?sort=default'.format(shop_name))
        time.sleep(random.random()*5 + 1)
        print(outside_code())
        totalpage = func_totalpage()
    return totalpage

def try_totalpage():
    try:
        totalpage = get_totalpage()
        return totalpage
    except:
        return try_totalpage()


def get_one_page(shop_name, i):
    print('---第',i,'页正在加载')
    url = 'https://{}.m.tmall.com/shop/shop_auction_search.do?ajson=1&_tm_source=tmallsearch&sort=s&p={}&page_size=12&from=h5&shop_id=57303596&callback=jsonp_{}'.format(shop_name, i, num)
    driver.get(url)
    time.sleep(random.random() + 1)
    html = driver.page_source
    if re.findall(r'\(({.*})\)', html):
        infos = re.findall(r'\(({.*})\)', html)[0]
        infos = json.loads(infos)
        products = infos.get('items')
        if products:
            for one_item in products:
                one_item['store_name'] = shop_name
                one_item['page'] = str(i)
        else:
            raise IndexError
    else:
        raise IndexError
    return products

# store_name = input('请输入店铺名： ')
def get_one_store():
    shop_name = shop_url[8:-12]
    all_page = []
    for i in range(1, totalpage+1):
        print('当前页面是: 第', i, '页')
        try:
            products = get_one_page(shop_name, i, num) #获取每页的数据
            all_page.extend(products)
            print('---第{}页加载完成\n'.format(i))
        except Exception:
    #         print(e)
            driver.get('{}/shop/shop_auction_search.htm?sort=default'.format(shop_url))
            time.sleep(random.random()*5 + 1)
            print(outside_code())  #如果需要滑动验证，进行滑动验证
            print(get_one_page(shop_name, i, num))
    df = pd.DataFrame(all_page)
    df.to_excel('D:\\Jupyter\\all_brand\\{}.xlsx'.format(brand_name))
    return '------{} finished!'

def try_one_store():
    try:
        print(get_one_store())
    except:
        return try_one_store()

def get_one_url():
    """从文件获取需要爬取的url链接"""
    url_file = r"D:\Python\TmallCrawler\file\Tmall_shop_lglat"
    with open(url_file, 'r', encoding='utf-8') as f:
        csv_reader = f.read().split('\n')
        for row in csv_reader:
            yield row.split('\t')

for i in get_one_url():
    brand_name, shop_url = i
    shop_name = shop_url[8:-12]
    print('{} is beginning'.format(brand_name))
    num = random.randint(1127482, 75727482)
    totalpage = try_totalpage()
    print('{} have {} page items'.format(brand_name, totalpage))