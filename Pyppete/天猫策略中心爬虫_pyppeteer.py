#!/usr/bin/env python
# coding: utf-8

import asyncio
import random

from pyppeteer import launch

login_url = r'https://strategy.tmall.com/welcome#/marketSeg/27647?_k=0zis0l'

loop = asyncio.get_event_loop()

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"

js1 = '''() =>{
    
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => undefined
             }
           })
        }'''
 
js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''
 
js3 = '''() => {
        window.navigator.chrome = {
    runtime: {},
    // etc.
  };
    }'''
 
js4 = '''() =>{
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
        }'''
 
js5 = '''() =>{
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
        }'''

# js6 = '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }'''
js7 = '''() =>{ window.navigator.chrome = { runtime: {},  }; }'''
# js8 = '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }'''
js9 = '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }'''


async def open_login():
    browser = await launch({
        'headless': False,
        'dumpio': True, #防止浏览器卡死
        'executablePath': "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        'args': ['--no-sandbox', '--disable-infobars', '--start-maximized']
    })
    page = await browser.newPage()
    await page.setViewport({'width': 1600, 'height': 900})
    await page.setUserAgent(useragent)
    await page.goto(login_url)
    # await page.evaluate(js1)
    # await page.evaluate(js3)
    # await page.evaluate(js4)
    # await page.evaluate(js5)
    # await page.evaluate(js7)
    await page_evaluate(page)
    iframe = [i for i in page.frames if i.name == 'tbLoginFrame'][0]
    await iframe.click('#J_Quick2Static')
    await iframe.waitFor(20)
    await iframe.type('#TPL_username_1','森马官方旗舰店:欣月', {'delay': 30})
    await  iframe.type('#TPL_password_1', 'semir2019', {'delay': 30})
    slider = await iframe.Jeval('#nocaptcha', 'node => node.style')
    await page_evaluate(page)
    if slider:
        print('出现滑块情况判定')
        # time.sleep(10)
        flag = await mouseslide(page=page, iframe=iframe)
        if flag:
            await get_cookie(page)

async def get_cookie(page):
    res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    print(cookies)
    return cookies

async def mouseslide(page=None, iframe=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await iframe.hover('#nc_1_n1z')
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

async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
    # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] }); }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5, 6], }); }''')


#     await browser.close()
#f'--window-size={width},{height}'

loop.run_until_complete(open_login())

