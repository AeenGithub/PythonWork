# -*- coding: utf-8 -*-
"""
@author: zhangslob
@file: taobao_login.py
@time: 2019/02/14
@desc:
"""

import asyncio
import json
import os
import random
import re
import time

import pandas as pd
from pyppeteer import errors
from pyppeteer import launch
from retrying import retry
from user_agent import generate_user_agent

config_file_dir = r"E:\SPiderFile\CsvResult"

async def taobao_login(username, password, url):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({
        'headless': False,
        'slowMo': 5,
        # 'devtools':True,
        'dumpio': True,  # 防止浏览器卡死
        # 'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'userDataDir ': 'D:\\UserData',
        # ["--enable-automation"],
        # 'useAutomationExtension':True,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--start-maximized',
            '--window-size=1920, 1080',
            '--proxy-server=http://127.0.0.1:9000'
        ]
    })
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3440.106 Safari/537.36')
    # 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36')
    await page.goto(url)
    await page.waitFor(1000)
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    # await page.evaluate('''() =>{ Object.defineProperties(navigator,{webdriver:{ get: () => false } }) }''')
    # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    # await page.click('#J_QRCodeLogin > div.login-links >
    # a.forget-pwd.J_Quick2Static')
    await page.click('#J_Quick2Static')
    # page.mouse
    # time.sleep(1)
    # 输入用户名，密码
    await page.waitFor(500)
    # delay是限制输入的时间
    await page.type('#TPL_username_1', username, {'delay': input_time_random() - 50})
    await page.type('#TPL_password_1', password, {'delay': input_time_random()})
    # time.sleep(2)
    await page.waitFor(500)
    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块

    if slider:
        print('当前页面出现滑块')
        # await page.screenshot({'path': './headless-login-slide.png'}) # 截图测试
        flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
        if flag:
            await page.keyboard.press('Enter')  # 确保内容输入完毕，少数页面会自动完成按钮点击
            print("print enter", flag)
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
            time.sleep(2)
            cookies_list = await page.cookies()
            print(cookies_list)
            # 导出cookie 完成登陆后就可以拿着cookie玩各种各样的事情了。
            return await get_cookie(page)
    else:
        print("")
        await page.keyboard.press('Enter')
        # print("print enter")
        # await
        # page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(1000)
        # await page.waitForNavigation()
        await page.setUserAgent(generate_user_agent(device_type='smartphone'))
        # await page.reload()
        await page.waitFor(1000)
        await get_store_info(page)
        try:
            global wrong_pwd_error  # 检测是否是账号密码错误
            # 错误内容是，账号密码出现错误
            wrong_pwd_error = await page.Jeval('.wrong_pwd_error', 'node => node.textContent')
            print("error_1:", wrong_pwd_error)
            print("error_2:", wrong_pwd_error)
        except Exception as e:
            wrong_pwd_error = None
        finally:
            if wrong_pwd_error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
                return await get_cookie(page)


# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    # print(cookies)
    return cookies


def page_source_resolve(page_source, store_name):
    if re.findall(r'\(({.*})\)', page_source):
        infos = re.findall(r'\(({.*})\)', page_source)[0]
        infos = json.loads(infos)
        try:
            totalpage = int(infos.get('total_page'))
            products = infos.get('items')
            if products:
                for one_item in products:
                    one_item['store_name'] = store_name
            return totalpage, products
        except TypeError as e:
            print(e, '登录后抓取数据时，需要重新验证')
            return None, None
    else:
        return None, None


async def get_store_info(page):
    with open(r"E:\SPiderFile\male_cowl_pants.csv", 'r', encoding='utf-8') as f:
        total_lst = f.read().split('\n')
        for one_row in total_lst:
            store_name = one_row.split('\t')[0]
            store_url = one_row.split('\t')[1]
            store_file_dir = '{}\\{}.csv'.format(config_file_dir, store_name)
            if os.path.exists(store_file_dir):
                print('{}已经存在了'.format(store_file_dir))
                continue
            try:
                    # 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36')
                await asyncio.wait([
                    page.goto(store_url),
                    page.waitForNavigation()
                ])
                # await page.waitFor(1500)
                await asyncio.wait([
                    page.click('#bodyCont > section.nav-bar-wrapper.J_tabNavBar > div > a:nth-child(2)'),
                    page.waitForNavigation(),
                ])
                # await page.waitFor(2500)
                await page.click('#J_order > div.o_item.J_itemSort.J_sortType_d')
                await asyncio.sleep(random.random() * 5)
                num = random.randint(10127482, 75727482)
                shop_name = page.url.split('.')[0].split('//')[1]
                first_page_url = '''https://{}.m.tmall.com/shop/shop_auction_search.do?ajson=1&_tm_source=tmallsear
                ch&sort=s&p=1&page_size=12&from=h5&shop_id=57303596&callback=jsonp_{}'''.format(shop_name, num)
                await page.goto(first_page_url)
                await page.waitFor(1500)
                page_source = await page.content()
                total_page, first_page_products = page_source_resolve(
                    page_source, store_name)
                if total_page:
                    # 根据网页上下载的数据，列表里的字典数据，选取字典的key作为表格的表头
                    cols = list(first_page_products[0].keys())
                    # 结合需要，增加两个新的表头
                    cols.extend(['total_page', 'page'])
                    # 讲数据从列表中套用字典的格式转为dataframe
                    first_page_df = pd.DataFrame(first_page_products)
                    first_page_df['total_page'] = total_page
                    first_page_df['page'] = 1
                    # 将第一页保存到本地
                    first_page_df.to_csv(
                        path_or_buf='{}\\{}.csv'.format(
                            config_file_dir,
                            store_name),
                        mode='a+',
                        encoding='utf-8',
                        columns=cols)
                    # 循环将后面所有页的数据都保存到本地
                    for one_page in range(2, total_page + 1):
                        page_url = 'https://{}.m.tmall.com/shop/shop_auction_search.do?ajson=1&_tm_source=tmallsearch&sort=s&p={}&page_size=12&from=h5&callback=jsonp_{}'.format(
                            shop_name, one_page, num)
                        await page.goto(page_url)
                        await page.waitFor(random.randint(3000, 8000))
                        one_page_source = await page.content()
                        total_page, products = page_source_resolve(
                            one_page_source, store_name)
                        if products:
                            one_page_df = pd.DataFrame(products)
                            one_page_df['total_page'] = total_page
                            one_page_df['page'] = one_page
                            one_page_df.to_csv(
                                path_or_buf='{}\\{}.csv'.format(
                                    config_file_dir,
                                    store_name),
                                mode='a+',
                                header=None,
                                encoding='utf-8',
                                columns=cols,
                            )
                        else:
                            # 如果出现错误，还没有完善
                            await page.goto(store_url)
                            await page.waitFor(1000)
                            await asyncio.sleep(5)
                            # await br
                            print('出现滑块，手动处理')
                            # page.close()
                            # await get_store_info(page)
            except errors.PageError as e:
                print('当前页面出现了错误', e)
                pass
                await asyncio.sleep(random.randint(1, 10))
                # time.sleep(random.randint(1,10))


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none)
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            # await page.screenshot({'path': './headless-slide-result.png'}) #
            # 截图测试
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    username = '17621780176'
    password = 'www.,194928.,com'
    url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(taobao_login(username, password, url))
    loop.run_until_complete(task)
    cookie = task.result()
    print(cookie)
