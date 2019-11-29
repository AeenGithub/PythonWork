# -*-coding:utf-8-*-
__author__ = 'AeenPython'

# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import asyncio
import json
import random
import re
import time

import pandas as pd
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的


async def main(username, pwd, url):  # 定义main协程函数，
    # dumpio:True 浏览器就不会卡住了
    # 启动pyppeteer 属于内存中实现交互的模拟器
    browser = await launch({
        'headless': False,
        'dumpio': True,  # 防止浏览器卡死
        'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'args': ['--no-sandbox', '--disable-infobars', '--window-size=1600, 900', '--allow-legacy-extension-manifests']
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
            else:
                break

        if flag:
            await page.keyboard.press('Enter')  # 确保内容输入完毕，少数页面会自动完成按钮点击
            print("print enter", flag)
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
            time.sleep(2)
            await get_cookie(page)
    else:
        print("")
        await page.keyboard.press('Enter')
        # print("print enter")
        # await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        await page.waitForNavigation()
        time.sleep(2)

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
                await get_cookie(page)
    await strategy_home_market(page, classid=28595) # 进入市场细分模块
    # await special_page_keywords(page, reportid=1278911)
    time.sleep(3)
    await special_page_wcloud(page, reportid=1278911)
    print('all is over')
    await page.close()
    time.sleep(1)
    await browser.close()


async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

async def strategy_home_market(page, classid=28595):
    url = 'https://strategy.tmall.com/#/marketOverview'
    await page.goto(url)
    await page_evaluate(page)
    await page.click('body > div > div.img-back > div:nth-child(2) > div > div > div > div > a > div')
    await page.waitFor(20)
    await page.waitForNavigation()
    await page.goto(f'https://strategy.tmall.com/#/marketSeg/{classid}')
    await page.waitFor(20)
    # await page.waitForSelector()
    time.sleep(random.randint(1, 5))
    await page.waitForSelector('#content_container', {'delay': input_time_random()})

async def special_page_keywords(page, reportid=1278911):
    keywords_url = f'https://strategy.tmall.com/api/scapi?&path=/quick/v1/marketOverviewReport/getKeywords&reportId={reportid}&date=2019&dateFlag=APPOINTED_DATE'
    keywords_url = r'https://strategy.tmall.com/api/scapi?&path=/quick/v1/marketOverviewReport/getKeywords&reportId=1278911&date=201904&dateFlag=ABSOLUTE_DATE_RANGE&customStartDate=201812'
    await page.goto(keywords_url) # 通过指定的关键词连接，获取关键词数据，包含销量和销额的绝对值等数据
    await page.waitFor(20)
    time.sleep(random.randint(1,5))
    page_source = await page.content()
    json_result = json.loads(re.findall(r'{.*}', page_source)[0])
    data_json = json_result['data']
    data_df = pd.DataFrame(data_json)
    data_df.columns = ['年份', '关键词', '商品个数','商品个数增长量', '商品个数同比', '商品个数同比率', '商品个数同比指', '支付平均价格',
                       '支付数量', '支付数量增长量', '支付数量同比', '支付数量同比值', '支付数量同期数量', '销售数量', '销售数量增长量',
                       '销售数量同比', '销售数量同比值', '销售数量同期量', '支付金额', '销售金额', '销售金额增长量', '销售金额同比',
                       '销售金额同比值', '销售金额同期量']
    data_df.to_excel('d:\\test\\男装-标题关键词-气泡图.xlsx', index=False)

async def special_page_wcloud(page, reportid=1278911):
    # keywords_url = f'https://strategy.tmall.com/api/scapi?&path=/quick/v1/marketOverviewReport/getSearchKeys&reportId={reportid}&date=2019&dateFlag=APPOINTED_DATE'
    keywords_url = 'https://strategy.tmall.com/api/scapi?path=/quick/v1/marketOverview/getSearchKeys&cateId=50008899&channelId=&date=201909&dateType=M'
    # keywords_url = r'https://strategy.tmall.com/api/scapi?path=/quick/v1/marketOverviewReport/getSearchKeys&reportId=1278911&cateId=50010402,50000436,50011123,50010158,50010167,50010159,3035,50010160,50011159,50011153&channelId=4&date=201904&dateType=Y&customStartDate=201812&dateFlag=ABSOLUTE_DATE_RANGE'
    await page.goto(keywords_url) # 通过指定的词云连接，获取词云中的关键词的具体数据
    page_source = await page.content()
    await page.waitFor(20)
    time.sleep(random.randint(1,5))
    json_result = json.loads(re.findall(r'{.*}', page_source)[0])
    data_json = json_result['data']
    data_df = pd.DataFrame(data_json)
    # data_df.columns = ['年份', '关键词', '搜索人数', '搜索人数同比', '搜索人数同比值', '搜索人数同期值', '转化率', '转化率同比', '转化率同比值', '转化率同期']
    data_df.to_excel('d:\\test\\女装羽绒服-搜索-转化率.xlsx', index=False)

# 获取登录后cookie
async def get_cookie(page):
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def retry_if_result_none(result):
    return result is None


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


if __name__ == '__main__':
    username = '森马官方旗舰店:欣月'  # 淘宝用户名
    pwd = 'semir2019'  # 密码
    # url = 'https://strategy.tmall.com/#/marketSeg/27647?_k=0zis0l'
    url = 'https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true&redirect_url=https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&reg= http://member.1688.com/member/join/enterprise_join.htm?lead=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&leadUrl=http://login.1688.com/member/'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    m = main(username, pwd, url)
    loop.run_until_complete(m)  # 将协程注册到事件循环，并启动事件循环





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