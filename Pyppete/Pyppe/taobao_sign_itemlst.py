# -*- coding: utf-8 -*-
'''
通过js的问题已经实现了下滑，然后中间件抓包，实现了需要的数据了，这个版本是比较稳定的了
'''
import asyncio
import json
import random

import js2py as jsp
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
        'devtools':True,
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
        await get_store_info(page)
        await page.close()
        await browser.close()
        # document_cookies = await page.cookies()
        # document_cookies =  await page.evaluate('''() => {return document.cookie}''')
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
    with open(r"E:\SPiderFile\c_store.csv", 'r', encoding='utf-8') as f:
        total_lst = f.read().split('\n')
        for one_row in total_lst:
            store_name = one_row.split(',')[0]
            store_url = one_row.split(',')[1]
            shop_id = one_row.split(',')[2]
            seller_id = one_row.split(',')[3]
            await asyncio.wait([
                page.goto(store_url),
                page.waitForNavigation(0)
            ])
#                点击并等待页面加载，点击宝贝列表，默认采用综合排序
            item_id_url = 'https://market.m.taobao.com/app/tb-source-app/shop-auction/pages/auction?w&sellerId={}&shopId={}&disablePromotionTips=false&shop_navi=allitems&displayShopHeader=true'.format(seller_id, shop_id)
            await asyncio.wait([
                page.goto(item_id_url),
                # '这里等待的设置还需要优化'
                page.waitForSelector('span')
            ])

            for i in range(1, 600):
                print('{}, 第{}次加载'.format(store_name, i))
                try:
                    # scrollIntoView
                    await asyncio.wait([
                        # 通过js执行下滑操作
                        page.evaluate('''() => {
    function aa() {
        var spanDoms = document.querySelectorAll("span"), domLen = spanDoms.length;
        for (var i = 0; i < domLen; i++) {
            var v = spanDoms[i]
            if (v.textContent === "加载中") {
                return v.scrollIntoView()
            }
        }
    }; return aa()
}'''),
                        # 当我需要的js链接出现，即可，经过测试发现，数据有些问题，等待时间过长，然后出现了错误
                        # page.waitForResponse(lambda res: 'appsearch' in str(res.url) and res.status == 200, options={'timeout':60})
                        # 直接等待所有的元素都加在完毕呢，反应加载时间过长
                        page.waitForSelector('span')
                        # page.waitForNavigation(options={'timeout':60})
                    ])
                    # 通过js判断加载中是否还在
                    load_span = await page.evaluate('''() => {
                        function aa() {
                            var spanDoms = document.querySelectorAll("span"), domLen = spanDoms.length;
                            for (var i = 0; i < domLen; i++) {
                                var v = spanDoms[i]
                                if (v.textContent === "加载中") {
                                    return v.textContent
                                }
                            }
                        }; return aa()
                    }''')
                    if load_span != '加载中':
                        # print('已经加载到底了')
                        break
                    # await asyncio.sleep( random.random())
                except Exception as e:
                    print(e)
                    continue
                finally:
                    print('{}, 第{}次加载完成\n'.format(store_name, i))
            # await asyncio.sleep(random.random() * 6)

def analys_sign(cookies, date_num, page_num):
    function_js = r'''function h(a) {
        function b(a, b) {
            return a << b | a >>> 32 - b
        }
        function c(a, b) {
            var c, d, e, f, g;
            return e = 2147483648 & a,
            f = 2147483648 & b,
            c = 1073741824 & a,
            d = 1073741824 & b,
            g = (1073741823 & a) + (1073741823 & b),
            c & d ? 2147483648 ^ g ^ e ^ f : c | d ? 1073741824 & g ? 3221225472 ^ g ^ e ^ f : 1073741824 ^ g ^ e ^ f : g ^ e ^ f
        }
        function d(a, b, c) {
            return a & b | ~a & c
        }
        function e(a, b, c) {
            return a & c | b & ~c
        }
        function f(a, b, c) {
            return a ^ b ^ c
        }
        function g(a, b, c) {
            return b ^ (a | ~c)
        }
        function h(a, e, f, g, h, i, j) {
            return a = c(a, c(c(d(e, f, g), h), j)),
            c(b(a, i), e)
        }
        function i(a, d, f, g, h, i, j) {
            return a = c(a, c(c(e(d, f, g), h), j)),
            c(b(a, i), d)
        }
        function j(a, d, e, g, h, i, j) {
            return a = c(a, c(c(f(d, e, g), h), j)),
            c(b(a, i), d)
        }
        function k(a, d, e, f, h, i, j) {
            return a = c(a, c(c(g(d, e, f), h), j)),
            c(b(a, i), d)
        }
        function l(a) {
            for (var b, c = a.length, d = c + 8, e = (d - d % 64) / 64, f = 16 * (e + 1), g = new Array(f - 1), h = 0, i = 0; c > i; )
                b = (i - i % 4) / 4,
                h = i % 4 * 8,
                g[b] = g[b] | a.charCodeAt(i) << h,
                i++;
            return b = (i - i % 4) / 4,
            h = i % 4 * 8,
            g[b] = g[b] | 128 << h,
            g[f - 2] = c << 3,
            g[f - 1] = c >>> 29,
            g
        }
        function m(a) {
            var b, c, d = "", e = "";
            for (c = 0; 3 >= c; c++)
                b = a >>> 8 * c & 255,
                e = "0" + b.toString(16),
                d += e.substr(e.length - 2, 2);
            return d
        }
        function n(a) {
            a = a.replace(/\r\n/g, "\n");
            for (var b = "", c = 0; c < a.length; c++) {
                var d = a.charCodeAt(c);
                128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(d >> 6 | 192),
                b += String.fromCharCode(63 & d | 128)) : (b += String.fromCharCode(d >> 12 | 224),
                b += String.fromCharCode(d >> 6 & 63 | 128),
                b += String.fromCharCode(63 & d | 128))
            }
            return b
        }
        var o, p, q, r, s, t, u, v, w, x = [], y = 7, z = 12, A = 17, B = 22, C = 5, D = 9, E = 14, F = 20, G = 4, H = 11, I = 16, J = 23, K = 6, L = 10, M = 15, N = 21;
        for (a = n(a),
        x = l(a),
        t = 1732584193,
        u = 4023233417,
        v = 2562383102,
        w = 271733878,
        o = 0; o < x.length; o += 16)
            p = t,
            q = u,
            r = v,
            s = w,
            t = h(t, u, v, w, x[o + 0], y, 3614090360),
            w = h(w, t, u, v, x[o + 1], z, 3905402710),
            v = h(v, w, t, u, x[o + 2], A, 606105819),
            u = h(u, v, w, t, x[o + 3], B, 3250441966),
            t = h(t, u, v, w, x[o + 4], y, 4118548399),
            w = h(w, t, u, v, x[o + 5], z, 1200080426),
            v = h(v, w, t, u, x[o + 6], A, 2821735955),
            u = h(u, v, w, t, x[o + 7], B, 4249261313),
            t = h(t, u, v, w, x[o + 8], y, 1770035416),
            w = h(w, t, u, v, x[o + 9], z, 2336552879),
            v = h(v, w, t, u, x[o + 10], A, 4294925233),
            u = h(u, v, w, t, x[o + 11], B, 2304563134),
            t = h(t, u, v, w, x[o + 12], y, 1804603682),
            w = h(w, t, u, v, x[o + 13], z, 4254626195),
            v = h(v, w, t, u, x[o + 14], A, 2792965006),
            u = h(u, v, w, t, x[o + 15], B, 1236535329),
            t = i(t, u, v, w, x[o + 1], C, 4129170786),
            w = i(w, t, u, v, x[o + 6], D, 3225465664),
            v = i(v, w, t, u, x[o + 11], E, 643717713),
            u = i(u, v, w, t, x[o + 0], F, 3921069994),
            t = i(t, u, v, w, x[o + 5], C, 3593408605),
            w = i(w, t, u, v, x[o + 10], D, 38016083),
            v = i(v, w, t, u, x[o + 15], E, 3634488961),
            u = i(u, v, w, t, x[o + 4], F, 3889429448),
            t = i(t, u, v, w, x[o + 9], C, 568446438),
            w = i(w, t, u, v, x[o + 14], D, 3275163606),
            v = i(v, w, t, u, x[o + 3], E, 4107603335),
            u = i(u, v, w, t, x[o + 8], F, 1163531501),
            t = i(t, u, v, w, x[o + 13], C, 2850285829),
            w = i(w, t, u, v, x[o + 2], D, 4243563512),
            v = i(v, w, t, u, x[o + 7], E, 1735328473),
            u = i(u, v, w, t, x[o + 12], F, 2368359562),
            t = j(t, u, v, w, x[o + 5], G, 4294588738),
            w = j(w, t, u, v, x[o + 8], H, 2272392833),
            v = j(v, w, t, u, x[o + 11], I, 1839030562),
            u = j(u, v, w, t, x[o + 14], J, 4259657740),
            t = j(t, u, v, w, x[o + 1], G, 2763975236),
            w = j(w, t, u, v, x[o + 4], H, 1272893353),
            v = j(v, w, t, u, x[o + 7], I, 4139469664),
            u = j(u, v, w, t, x[o + 10], J, 3200236656),
            t = j(t, u, v, w, x[o + 13], G, 681279174),
            w = j(w, t, u, v, x[o + 0], H, 3936430074),
            v = j(v, w, t, u, x[o + 3], I, 3572445317),
            u = j(u, v, w, t, x[o + 6], J, 76029189),
            t = j(t, u, v, w, x[o + 9], G, 3654602809),
            w = j(w, t, u, v, x[o + 12], H, 3873151461),
            v = j(v, w, t, u, x[o + 15], I, 530742520),
            u = j(u, v, w, t, x[o + 2], J, 3299628645),
            t = k(t, u, v, w, x[o + 0], K, 4096336452),
            w = k(w, t, u, v, x[o + 7], L, 1126891415),
            v = k(v, w, t, u, x[o + 14], M, 2878612391),
            u = k(u, v, w, t, x[o + 5], N, 4237533241),
            t = k(t, u, v, w, x[o + 12], K, 1700485571),
            w = k(w, t, u, v, x[o + 3], L, 2399980690),
            v = k(v, w, t, u, x[o + 10], M, 4293915773),
            u = k(u, v, w, t, x[o + 1], N, 2240044497),
            t = k(t, u, v, w, x[o + 8], K, 1873313359),
            w = k(w, t, u, v, x[o + 15], L, 4264355552),
            v = k(v, w, t, u, x[o + 6], M, 2734768916),
            u = k(u, v, w, t, x[o + 13], N, 1309151649),
            t = k(t, u, v, w, x[o + 4], K, 4149444226),
            w = k(w, t, u, v, x[o + 11], L, 3174756917),
            v = k(v, w, t, u, x[o + 2], M, 718787259),
            u = k(u, v, w, t, x[o + 9], N, 3951481745),
            t = c(t, p),
            u = c(u, q),
            v = c(v, r),
            w = c(w, s);
        var O = m(t) + m(u) + m(v) + m(w);
        return O.toLowerCase()
    }'''
    d_token_func = r'''function j(a, document_cookie) {
            var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(document_cookie);
            return b ? b[1] : void 0
        }'''
    func_js = jsp.eval_js(function_js)
    d_token_func_a = jsp.eval_js(d_token_func)
    a = '_m_h5_tk'
    g = '12574478'
    a_token = d_token_func_a(a, cookies)
    a_token = a_token.split("_")[0]
    page_str = "{}".format(page_num)
    c_data = {"m": "shopitemsearch", "vm": "nw", "sversion": "4.6", "shopId": "111126855", "sellerId": "2103587316",
               "style": "wf", "page": page_str, "sort": "_coefp", "catmap": "", "wirelessShopCategoryList": ""}
    json_c_data = json.dumps(c_data)
    abss_arg = a_token + "&" + date_num + "&" + g + "&" + json_c_data.replace(' ', '')
    return func_js(abss_arg)


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