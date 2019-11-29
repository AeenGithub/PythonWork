# -*- coding: utf-8 -*-
'''
通过js的问题已经实现了下滑，然后中间件抓包，实现了需要的数据了，这个版本是比较稳定的了
'''
import asyncio
import random

from pyppeteer import launch
from retrying import retry
from user_agent import generate_user_agent

# os.environ['PYTHONASYNCIODEBUG'] = '1'
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
        'slowMo': 25,
        'devtools': True,
        'dumpio': True,  # 防止浏览器卡死
        # 'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'userDataDir ': 'D:\\UserData\\Default',
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
            # time.sleep(2)
            cookies_list = await page.cookies()
            document_cookies = await get_cookie(page)
            print(cookies_list)
            # 导出cookie 完成登陆后就可以拿着cookie玩各种各样的事情了。
            return await get_cookie(page)
    else:
        print("")
        await page.keyboard.press('Enter')
        await page.waitFor(1000)
        await page.setUserAgent(generate_user_agent(device_type='smartphone'))
        await page.setViewport({'width': 360, 'height': 640, 'isMobile': True})
        await page.waitFor(1000)
        # document_cookies = await page.evaluate('''() => {return document.cookie}''')
        await get_store_info(page)
        await page.close()
        await browser.close()
        # document_cookies = await page.cookies()
        document_cookies =  await page.evaluate('''() => {return document.cookie}''')
        # page_num = 1
        # date_num = str(int((datetime.now() - datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')).total_seconds() * 1000))
        # sign = analys_sign(document_cookies, date_num, page_num)
        # print(date_num, sign)
        # shop_id = '111126855'
        # page_url = '''https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.2&appKey=12574478&t={}&sign={}&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&AntiCreep=true&type=jsonp&timeout=3000&dataType=jsonp&callback=mtopjson{}5&data=%7B%22m%22%3A%22shopitemsearch%22%2C%22vm%22%3A%22nw%22%2C%22sversion%22%3A%224.6%22%2C%22shopId%22%3A%22{}%22%2C%22sellerId%22%3A%222103587316%22%2C%22style%22%3A%22wf%22%2C%22page%22%3A1%2C%22sort%22%3A%22_sale%22%2C%22q%22%3A%22%22%2C%22catmap%22%3A%22%22%2C%22wirelessShopCategoryList%22%3A%22%22%7D'''.format(date_num, sign, page_num, shop_id)
        # await page.goto(page_url)
        # await page.waitFor(2000)
        # page_source = await page.content()
        # if 'mtopjson15' in page_source:
        #     await page.close()
        #     await browser.close()
        # try:
        #     global wrong_pwd_error  # 检测是否是账号密码错误
        #     # 错误内容是，账号密码出现错误
        #     wrong_pwd_error = await page.Jeval('.wrong_pwd_error', 'node => node.textContent')
        #     print("error_1:", wrong_pwd_error)
        #     print("error_2:", wrong_pwd_error)
        # except Exception as e:
        #     print(e)
        #     wrong_pwd_error = None
        # finally:
        #     if wrong_pwd_error:
        #         print('确保账户安全重新入输入')
        #         # 程序退出。
        #         loop.close()
        #     else:
        #         print(page.url)
        #         return await get_cookie(page)


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


async def get_store_info(page):
    with open(r"E:\SPiderFile\store_search.csv", 'r', encoding='utf-8') as f:
        total_lst = f.read().split('\n')
        for store_name in total_lst:
            search_url = 'http://shop.m.taobao.com/shop/shop_search.htm?q={}&_input_charset=utf-8&topSearch=1&atype=b&sid=&searchfrom=&action=RedirectAppAction&event_submit_do_search_shop=%E6%90%9C+%E7%B4%A2'.format(store_name)
            await asyncio.wait([
                page.goto(search_url),
                page.reload(),
                page.waitForNavigation(0)
            ])
            try:
                store_url = await page.querySelectorEval("#J_SearchList > ul > li:nth-child(1) > a", 'node => node.href')
            except:
                print('wrong, one')
                store_url = await page.evaluate('''() => {return document.querySelector("#J_SearchList > ul > li:nth-child(1) > a").href}''')
            with open(r"E:\SPiderFile\store_url.csv", 'a+', encoding='utf-8') as f:
                f.write(','.join([store_name, store_url]))
                f.write('\n')

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
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    username = '17621780176'
    password = 'www.,194928.,com'
    url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    task = asyncio.ensure_future(taobao_login(username, password, url))
    loop.run_until_complete(task)
    cookie = task.result()
    print(cookie)

# await page.goto(first_page_url)
# await page.waitFor(1500)
# page_source = await page.content()
# total_page, one_page_df = page_source_resolve(page_source, store_name)
# if total_page:
#     one_page_df.to_csv('{}\\{}.csv'.format(config_file_dir, store_name),
#                        mode='a+',
#                        encoding='utf-8',
#                        )
#                    page.click(selector='body > div.rax-scrollview > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(2) > span',
#                               options={'delay': input_time_random()}),
#                 page.waitForNavigation()
#     # 循环将后面所有页的数据都保存到本地
#     for one_page in range(2, total_page + 1):
#         page_url = '''https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.2&appKey=12574478&t={}&sign=c029ffcece874002f2b552a9c822b524&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&AntiCreep=true&type=jsonp&timeout=3000&dataType=jsonp&callback=mtopjsonp5&data=%7B%22m%22%3A%22shopitemsearch%22%2C%22vm%22%3A%22nw%22%2C%22sversion%22%3A%224.6%22%2C%22shopId%22%3A%22{}%22%2C%22sellerId%22%3A%222103587316%22%2C%22style%22%3A%22wf%22%2C%22page%22%3A1%2C%22sort%22%3A%22_sale%22%2C%22q%22%3A%22%22%2C%22catmap%22%3A%22%22%2C%22wirelessShopCategoryList%22%3A%22%22%7D'''.format(datenum, shop_id)
#         await page.goto(page_url)
#         await page.waitFor(random.randint(3000, 8000))
#         one_page_source = await page.content()
#         total_page, products = page_source_resolve(
#             one_page_source, store_name)
#         if products:
#             one_page_df = pd.DataFrame(products)
#             one_page_df['total_page'] = total_page
#             one_page_df['page'] = one_page
#             one_page_df.to_csv('{}\\{}.csv'.format(config_file_dir, store_name),
#                                mode='a+',
#                                header=None,
#                                encoding='utf-8'
#                                )
#         else:
#             # 如果出现错误，还没有完善
#             await page.goto(store_url)
#             await page.waitFor(1000)
#             await asyncio.sleep(5)
#             # await br
#             print('出现滑块，手动处理')
#             # page.close()
#             # await get_store_info(page)
# except errors.PageError as e:
# print('当前页面出现了错误', e)
# pass
# await asyncio.sleep(random.randint(1, 10))
# # time.sleep(random.randint(1,10))
#-*-coding:utf-8-*-
__author__ = 'AeenPython' 