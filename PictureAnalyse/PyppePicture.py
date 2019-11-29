# -*-coding:utf-8-*-
__author__ = 'AeenPython'

# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import asyncio
import json
import pickle
import random
import re
import time

import pandas as pd
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from qiniu import Auth, BucketManager
from retrying import retry  # 设置重试次数用的


async def main(loop, username, pwd, url):  # 定义main协程函数，
    # dumpio:True 浏览器就不会卡住了
    # 启动pyppeteer 属于内存中实现交互的模拟器
    browser = await launch({
        'headless': False,
        'dumpio': True,  # 防止浏览器卡死
        'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'args': ['--no-sandbox', '--disable-infobars', '--window-size=1600, 900']
    })
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setViewport({'width': 1600, 'height': 900}) # 设置整个页面的大小
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36')
    await page.goto(url)  # 访问登录页面
    await page_evaluate(page)
    # await page.evaluate('function resetBtn(){$("#name").val("");}')
    await page.type('.J_UserName', username, {'delay': input_time_random() - 50})
    await page.type('#J_StandardPwd input', pwd, {'delay': input_time_random()})
    await page.waitFor(2)
    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
    if slider:
        print('当前页面出现滑块')
        while True:
            print('刷新')
            # 用于滑动失败刷新
            flag, page = await mouse_slide(page=page)
            fresh = ''
            try:
                fresh = await page.Jeval('.errloading', 'node => node.textContent')
            except:
                pass
            if fresh:
                await page.hover('a[href="javascript:noCaptcha.reset(1)"]')
                await page.mouse.down()
                await page.mouse.up()
                time.sleep(1)
                await pailitao_home(page)
                cookies_dict = await get_cookie(page)
                with open('taobao_cookies.pickle', 'wb') as f:
                    f.write(pickle.dumps(cookies_dict))
            else:
                break
        if flag:
            await page.keyboard.press('Enter')  # 确保内容输入完毕，少数页面会自动完成按钮点击
            print("print enter", flag,'已经成功登陆到1688网')
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
            # time.sleep(2)
            # await pailitao_home(page)
            # cookies_dict = await get_cookie(page)
            # with open('taobao_cookies.pickle', 'wb') as f:
            #     f.write(pickle.dumps(cookies_dict))
    else:
        print("")
        await page.keyboard.press('Enter')
        print("print enter")
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        await page.waitForNavigation()
        time.sleep(2)
        # await pailitao_home(page)
        try:
            global error  # 检测是否是账号密码错误
            print("error_1:", error)
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error_2:", error)
        except Exception as e:
            error = None
        finally:
            if error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
    cookies_dict =  await get_cookie(page)  #获取cookies
    with open('taobao_cookies.pickle', 'wb') as f:
        f.write(pickle.dumps(cookies_dict))
    return browser, page
    # await browser.close()

def get_file_fron_qiniu():
    one_pic_lst = []
    host = 'http://ptn9z2j0m.bkt.clouddn.com'
    # bucket_domain = host[7:]
    access_key = 'Amsb0VBTxOJBlCAhcSmRxA4O8gPLde6MBHoC_UdM'
    secret_key = 'Jl-F0fqFTSzzHWLRa4rTkxnuQw4mZNAPWXtSZ5Pz'
    # 初始化Auth状态
    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)
    # 你要测试的空间， 并且这个key在你空间中存在
    bucket_name = '0614consumer'
    # 前缀
    prefix = None
    # 列举条目
    limit = 2549
    delimiter = None
    # 标记
    marker = None
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
    for one_pic in ret['items']:
        one_pic_lst.append(host + '/' + one_pic['key'])
    return one_pic_lst


async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

# picture_url = 'http://pr7q5c5ea.bkt.clouddn.com/IMG_20190412_192321-objectsperson-2.jpg'
async def pailitao_home(page, picture_url):
    # await page.waitForNavigation()
    await asyncio.sleep(2)
    url = 'http://www.pailitao.com'
    await page.goto(url)
    await page.waitFor(3)
    await page.type('#q', picture_url)
    await page.keyboard.press('Enter')
    # await page.waitFor(20)
    try:
        await page.waitForSelector('#imgsearch-header > div > div > div > div.markets.icon-tag.J_HeaderMarket > div.label > span:nth-child(1)')
    except:
        print('出现错误')
        pass
    # await page.waitForNavigation()
    title = await page.title()
    if title == 'security-X5':
        print('出现滑块验证')
        await securityX5(page)
        time.sleep(random.randint(1, 5))
        await page_evaluate(page)
        # await page.goto(url)
        await page.type('#q', picture_url)
        await page.keyboard.press('Enter')
    else:
        pass
    # await page.waitForNavigation()
    await page.waitFor(5)
    await page.waitForSelector('#imgsearch-header > div > div > div > div.markets.icon-tag.J_HeaderMarket > div.label > span:nth-child(1)')

async def save_data_from_web(page, picture_url):
    print('{}正在访问中'.format(picture_url))
    page_html = await page.content()
    str_dict = re.findall('g_page_config = (.*?);\n', page_html)
    if str_dict:
        json_data = json.loads(str_dict[0])
        with open('json_data', 'wb') as f:
            f.write(pickle.dumps(json_data))
        if json_data['mods'].get('itemlist'):
            similar_auctions = json_data['mods']['itemlist']['data']['collections'][0]['auctions']
            last_lst = []
            for one_aution_dict in similar_auctions:
                one_new_dict = {}
                one_new_dict['[temid'] = one_aution_dict['nid']
                one_new_dict['category'] = one_aution_dict['category']
                one_new_dict['title'] = one_aution_dict['title']
                one_new_dict['detail_url'] = one_aution_dict['detail_url']
                last_lst.append(one_new_dict)
            df = pd.DataFrame(last_lst)
            df['picture'] = picture_url
            df.to_csv('../PictureAnalyse/similar_itemId100.csv', encoding='utf-8', mode='a+')
            print('{}数据保存成功'.format(picture_url))
        else:
            print('没有数据，识别失败')
            with open('failed', 'w') as f:
                f.write(picture_url)
                f.write('\n')


async def pailitao_main(browser, page):
    # picture_url = 'http://pr7q5c5ea.bkt.clouddn.com/IMG_20190412_192321-objectsperson-2.jpg'
    for picture_url in get_file_fron_qiniu():
        await pailitao_home(page, picture_url)
        await page.waitFor(3)
        await save_data_from_web(page, picture_url)
        await page.waitFor(2)
        await asyncio.sleep(5)
    await browser.close()


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def securityX5(page):
    await asyncio.sleep(2)
    await page_evaluate(page)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = ''
        try:
            slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        except:
            pass
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page

# 获取登录后cookie
async def get_cookie(page):
    new_cookies = {}
    cookies_list = await page.cookies()
    for cookie in cookies_list:
        new_cookies[cookie.get('name')] = cookie.get('value')
    return new_cookies


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None, frame=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        if frame:
            await frame.hover('#nc_1_n1z')
        else:
            await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = ''
        try:
            slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        except:
            pass
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)

# def last_main():
#     username = '17621780176'  # 淘宝用户名
#     pwd = 'www.,194928.,com'  # 密码
#     url = 'https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true&redirect_url=https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&reg= http://member.1688.com/member/join/enterprise_join.htm?lead=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&leadUrl=http://login.1688.com/member/'
#     loop1 = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
#     m = main(loop1, username, pwd, url)
#     task_login = asyncio.ensure_future(m)
#     loop1.run_until_complete(task_login)
#     new_page = task_login.result()
#     loop2 = asyncio.get_event_loop()
#     tasks = []
#     all_picture_url = get_file_fron_qiniu()
#     for picture_url in get_file_fron_qiniu():
#         tasks.append(asyncio.ensure_future(pailitao_main(new_page, picture_url)))
#     loop2.run_until_complete(tasks)


    # loop.run_until_complete()


if __name__ == '__main__':
    username = '17621780176'  # 淘宝用户名
    pwd = 'www.,194928.,com'  # 密码
    url = 'https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true&redirect_url=https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&reg= http://member.1688.com/member/join/enterprise_join.htm?lead=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&leadUrl=http://login.1688.com/member/'
    loop1 = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    m = main(loop1, username, pwd, url)
    task_login = asyncio.ensure_future(m)
    loop1.run_until_complete(task_login)
    # loop1.close()
    browser, new_page = task_login.result()
    loop2 = asyncio.get_event_loop()
    task2 = asyncio.ensure_future(pailitao_main(browser, new_page))
    loop2.run_until_complete(task2)




# async def spider_search(browser, page):
#     url = 'strategy.tmall.com/#/marketSeg/27647?_k=0zis0l'
#     await page.goto(url)
#     await page_evaluate(page)
#     page_num = 0
#     while page_num < 5:
#         print(page_num + 1)
#         time.sleep(0.5)
#         # 这里选择通过构造url来翻页，这样对于可能出现的滑块验证就存在于page中
#         # 如果选择通过点击页面的翻页按钮翻页，则会在当前页面弹出一个小框滑动验证，此时需要检查页面的frames,找到弹出的框才能定位到滑块
#         url = 'https://s.taobao.com/search?spm=a21bo.2017.201856-fline.3.5af911d9CJTHFx&q=T%E6%81%A4&refpid=420462_1006&source=tbsy&style=grid&tab=all&pvid=d0f2ec2810bcec0d5a16d5283ce59f67&bcoffset=0&p4ppushleft=3%2C44&s={0}'.format(
#             44 * page_num)
#         await page.goto(url)
#         # 由于重新跳转了页面，window.navigator.webdriver的值被改为了True，需要再次设置为undefined，否则翻页过程中出现滑块，则会一直滑动失败
#         await page_evaluate(page)
#         try:
#             slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
#             if slider:
#                 while True:
#                     print('刷新')
#                     # 用于滑动失败刷新
#                     flag, page = await mouse_slide(page=page)
#                     fresh = ''
#                     try:
#                         fresh = await page.Jeval('.errloading', 'node => node.textContent')
#                     except:
#                         pass
#                     if fresh:
#                         await page.hover('a[href="javascript:noCaptcha.reset(1)"]')
#                         await page.mouse.down()
#                         await page.mouse.up()
#                         time.sleep(1)
#                     else:
#                         break
#         except Exception as e:
#             print(e)
#             pass
#         page_num += 1
#     print('over')