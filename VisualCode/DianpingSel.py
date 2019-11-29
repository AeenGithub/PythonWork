# coding: utf-8

import csv
import math
import random
import re
import time

import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


class DianPingSpider(object):
    def __init__(self):
        # self.have_data = self.compare_down_data()
        self.header_css = {
            'Host': 's3plus.meituan.net',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        self.iframe = (By.TAG_NAME, 'iframe')

    def start_driver(self):
        '''启动firefox57,设置firefox的请求头'''
        random_user_agent = generate_user_agent(os=('win', 'linux'))
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", random_user_agent)
        fp.update_preferences()
        shopdriver = webdriver.Firefox(firefox_profile=fp)
        return shopdriver

    def dianping_login(self, shopdriver):
        shopdriver.get('http://account.dianping.com/login')
        print(input('请扫描屏幕二维码登录'))
        return 'ok, 登陆成功了!'

    def get_dianping_provinces(self, shopdriver):
        '''访问大众点评城市列表,获取所有的城市列表和的对应的森马门店链接'''
        shopdriver.get('http://www.dianping.com/citylist')
        shopdriver.find_element_by_css_selector('#main > div.underline.province > div.choose-city > div > div.province-choose > p').click()
        all_provinces = shopdriver.find_elements_by_css_selector('#main > div.underline.province > div.choose-city > div > div.province-choose > div > div > span')
        # 获取所有的省份列表
        total_provinces = len(all_provinces)
        for index in range(1, total_provinces + 1):
            # 点击省份下拉框列表
            shopdriver.find_element_by_css_selector('#main > div.underline.province > div.choose-city > div > div.province-choose > p').click()
            # 获取其中某个省份的名称
            name_css_selector = '#main > div.underline.province > div.choose-city > div > div.province-choose > div > div > span:nth-child({index})'.format(index=index)
            province_name = shopdriver.find_element_by_css_selector(name_css_selector).text
            # 选择某个省份
            province_select_js = '''document.querySelector('#main > div.underline.province > div.choose-city > div > div.province-choose > div > div > span:nth-child({index})').click()'''.format(index=index)
            # 不知什么原因,导致用js无法获得省份名称,只能用selenium定位元素
            #     province_name_js = '''return document.querySelector('#main > div.underline.province > div.choose-city > div > div.province-choose > div > div > span:nth-child({index})').innerText;'''.format(index=index)
            #     province_name = shopdriver.execute_script(province_name_js)
            shopdriver.execute_script(province_select_js)
            #     shopdriver.implicitly_wait(10)
            time.sleep(2)
            # 再选择一个省份之后,点击获取城市的清单
            shopdriver.find_element_by_css_selector('#main > div.underline.province > div.choose-city > div > div.city-choose').click()
            citys = shopdriver.find_elements_by_css_selector('#main > div.underline.province > div.choose-city > div > div.city-choose > div > div > a')
            # 循环获取每一个城市的名称和对应链接
            time.sleep(3)
            for city_index in range(1, len(citys) + 1):
                #         city_name_js = '''return document.querySelector('#main > div.underline.province > div.choose-city > div > div.city-choose > div > div > a:nth-child({city_index})').innerText'''.format(city_index=city_index)
                #         one_city_name = shopdriver.execute_script(city_name_js)
                # 获取城市列表中的城市名称
                city_css_selector = '#main > div.underline.province > div.choose-city > div > div.city-choose > div > div > a:nth-child({index})'.format(index=city_index)
                one_city_name = shopdriver.find_element_by_css_selector(city_css_selector).text
                # 获得城市列表中每个城市的链接
                one_city_href = shopdriver.find_element_by_css_selector(city_css_selector).get_attribute('href')
                #         city_click_js = '''document.querySelector('#main > div.underline.province > div.choose-city > div > div.city-choose > div > div > a:nth-child({index})').click()'''.format(index=city_index)
                #         shopdriver.execute_script(city_click_js)
                # 将访问获得的城市链接保存本地
                with open('d:\\test\\dianping_provinces', 'a+', encoding='utf-8') as f:
                    if one_city_name != '':
                        one_row = '{}, {}, {}\n'.format(province_name, one_city_name, one_city_href)
                        print(one_row)
                        f.write(one_row)
                yield province_name, one_city_name, one_city_href

    def search_semir_new_window(self, one_city_href, shopdriver):
        shopdriver.get(one_city_href)
        default_handle = shopdriver.current_window_handle
        search_input = (By.ID, 'J-search-input')
        input_box = WebDriverWait(shopdriver, 5).until(EC.presence_of_element_located(search_input))
        input_box.clear()
        try:
            shopdriver.implicitly_wait(10)
            shopdriver.find_element_by_id('J-search-input').send_keys('森马')
            shopdriver.find_element_by_id('J-all-btn').click()
        except exceptions.NoSuchElementException as e:
            print('搜索框无法搜索到')
        print('搜索跳转成功,开始循环抓取店铺列表\n')
        return default_handle

    def get_total_semir_href(self, shopdriver):
        for province_name, one_city_name, one_city_href in self.get_dianping_provinces(shopdriver):
            default_handle = self.search_semir_new_window(one_city_href, shopdriver)
            handles = shopdriver.window_handles
            if len(handles) >= 2:
                handles.remove(default_handle)
                search_handle = handles[0]
                shopdriver.switch_to.window(search_handle)
            time.sleep(random.random() * 5)
            total_shop_contents = shopdriver.find_element_by_css_selector('body > div.section.Fix.J-shop-search > div.bread.J_bread > span:nth-child(3)').text
            total_shop_counts = int(re.findall('[0-9]{1,10}', total_shop_contents)[0])
            shop_lst_pages = math.ceil(total_shop_counts / 15)
            real_url = shopdriver.current_url
            one_city = []
            for i in range(1, shop_lst_pages + 1):
                page_url = real_url + '/p' + str(i)
                shopdriver.get(page_url)
                time.sleep(random.random() * 5)
                total_shops = shopdriver.find_elements_by_css_selector('#shop-all-list > ul > li')
                for one_shop in total_shops:
                    one_shop_href = one_shop.find_element_by_css_selector('div.pic > a').get_attribute('href')
                    one_shop_title = one_shop.find_element_by_css_selector('div.txt > div.tit > a').get_attribute(
                        'title')
                    one_shop_comment_star = one_shop.find_element_by_css_selector(
                        'div.txt > div.comment > span').get_attribute('title')
                    one_shop_comment_href = one_shop.find_element_by_css_selector(
                        'div.txt > div.comment > a').get_attribute('href')
                    one_city.append((one_shop_href, one_shop_title, one_shop_comment_star))
                    with open('d:\\test\\dianping_semir', 'a+', encoding='utf-8') as f:
                        one_row = '{}, {}, {}, {}, {}, {}\n'.format(province_name, one_city_name, total_shop_counts,
                                                                    one_shop_href, one_shop_title,
                                                                    one_shop_comment_star)
                        print(one_row)
                        f.write(one_row)
            shopdriver.close()
            shopdriver.switch_to.window(default_handle)

    def pinglun_deal(self, data):
        #     每一条评论的提取,删除评论中不需要的信息
        pinglun = data("div.review-words.Hide").html()
        try:
            len(pinglun)
        except:
            pinglun = data("div.review-words").html()
        less_words_loc = pinglun.find('less-words')
        if less_words_loc != -1:
            pinglun = pinglun[:less_words_loc - 14]
        return pinglun

    def css_get(self, doc):
        total_lst_dict = {}
        css_link = "http:" + doc("head > link:nth-child(9)").attr("href")
        background_link = requests.get(css_link, headers=self.header_css, timeout=30)
        css_text = background_link.text
        r = r'background-image: url(.*?);'
        r2 = r'(background-image: url.*?;)'
        need_replace_text = re.findall(r2, css_text)
        total_matches = re.findall(r, background_link.text)
        for i in need_replace_text:
            css_text = css_text.replace(i, '')
        total_lst = []
        if total_matches:
            for one_match in total_matches:
                svg_link = one_match.replace(")", "").replace("(", "http:")
                status, list_svg_y = self.svg_text(svg_link)
                total_lst.extend(list_svg_y)
        # 对css进行解析,明白css中background对应的坐标的数据的转换
        dict_css = self.css_dict(css_text)
        for x, y, c in total_lst:
            total_lst_dict[y] = (x, c)
        return total_lst_dict, dict_css

    # 2-字体库链接和字体库
    def svg_text(sefl, url):
        html = requests.get(url, timeout=30)
        svg_text_r2 = r'<text x="(.*?)" y="(.*?)">(.*?)</text>'
        svg_text_re = re.findall(svg_text_r2, html.text)
        if svg_text_re:
            return 1, svg_text_re
        else:
            svg_text_r = r'<textPath xlink:href="(.*?)" textLength="(.*?)">(.*?)</textPath>'
            svg_text_re = re.findall(svg_text_r, html.text)
            dict_avg = {}
            # 生成svg加密字体库字典
            for data in svg_text_re:
                dict_avg[data[0].replace("#", "")] = list(data[2])
            svg_y_r = r'<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>'
            svg_y_re = re.findall(svg_y_r, html.text)
            list_y = []
            # 存储('18', 'M0', '748', 'H600') eg:(x坐标，未知，y坐标，未知)
            for data in svg_y_re:
                list_y.append([data[0], data[2]])
            res_yindex_words = []
            for index, one_y in enumerate(list_y):
                mixed_words = ''.join(dict_avg[str(index + 1)])
                one_y.append(mixed_words)
                res_yindex_words.append(one_y)
            return 2, res_yindex_words

    # 3-生成css字库字典
    def css_dict(self, html):
        css_text_r = r'.([a-zA-Z0-9]{1,6}){background:(.*?)px (.*?)px;}'
        css_text_re = re.findall(css_text_r, html)
        dict_css = {}
        for data in css_text_re:
            """
            加密字库.gqi4j {background: -98.0px -745.0px;}与svg文件对应关系，x/14，就是svg文件加密字体下标
            y，原样返回，需要在svg函数中做处理
            """
            x = int(float(data[1]) / -14)
            y = -int(float(data[2]))
            dict_css[data[0]] = (data[1], data[2], x, y)
        return dict_css

    def css_decode(self, total_lst_dict, dict_css, pinglun):
        #     每一条评论数据,将其字符串化,然后删除掉不需要的信息
        pinglun_text = pinglun.replace('<svgmtsi class="', ',').replace('"/>', ",").replace('">', ",")
        pinglun_list = [x.strip('\n').strip(' ') for x in pinglun_text.split(",") if x != '']
        pinglun_list = [x for x in pinglun_list if x != '']
        #     获取加密后的所有文字列表
        encryt_words_lst = list(dict_css.keys())
        #     循环每个字符,对加密的字符,匹配解密
        pinglun_str = []
        for msg in pinglun_list:
            # 如果有加密标签
            if msg in encryt_words_lst:
                # 参数说明：[x,y] css样式中background 的[x/14，y]
                x = dict_css[msg][2]
                y = dict_css[msg][3]
                for g in total_lst_dict.keys():
                    if y < int(g):
                        try:
                            pinglun_str.append(total_lst_dict[g][1][x])
                            break
                        except IndexError:
                            pinglun_str.append(' ')
                            break
            # 没有加密标签
            else:
                pinglun_str.append(msg.replace("\n", ""))
        #     将所有的解密后的字符,拼接起来.得到真实评论数据
        if pinglun_str:
            str_pinglun = ''.join(pinglun_str)
            # 删除掉所有的空格数据
            str_pinglun = str_pinglun.strip(' ')
        else:
            str_pinglun = ''
        return str_pinglun

    def down_one_shop_comments(self, shopdriver, have_data):
        fieldnames = ['province_name', 'city_name', 'one_city_one_shop_url', 'one_city_one_shop_name', 'userName',
                      'userID', 'startShop', 'describeShop', 'pinglunTime', 'pinglun']
        # 对于已经下载的大众点评的所有森马门店数据重新读入(这里筛选了没有星级评分的店铺)
        with open(r"D:\Test\dazhongdianping_semir_address.csv", 'r', encoding='utf-8') as f:
            total_rows = f.read().split('\n')
        # 将每一条记录变成列表
        # file = [i.split(',') for i in total_rows]
        # file =  self.have_data
        file = have_data
        for province_name, city_name, total_shops, one_city_one_shop_url, one_city_one_shop_name, shop_stars in file:
            # 根据实际情况,得到所有的评论链接,后缀为 "/review_all",所有点评的页面的数据的加密方式比较一致
            review_all_url = one_city_one_shop_url + '/review_all'
            shopdriver.get(review_all_url)
            shopdriver.implicitly_wait(30)
            time.sleep(2)
            try:
                # 读取页面上评论计数，并将文字描述中的数字提取出来，当作总评论数，根据每页15条评论，计算出总页数
                comments_contents = shopdriver.find_element_by_css_selector('html > body > div#index-main >  div#review-list.review-list > div.review-list-container > div.review-shop-wrap > div.rank-info span.reviews').text
                comment_count = int(re.findall('[0-9]{1,10000}', comments_contents)[0])
                commnet_pages = math.ceil(comment_count / 15)
                print('{}一共有{}页{}条评论'.format(one_city_one_shop_name, commnet_pages, comment_count))
                # 如果评论为0，直接跳过，对下一个门店继续操作
                if comment_count == 0:
                    one_comment_dict = {
                        "province_name": province_name,
                        "city_name": city_name,
                        "one_city_one_shop_url": one_city_one_shop_url,
                        "one_city_one_shop_name": one_city_one_shop_name,
                        "userName": '',
                        "userID": '',
                        "startShop": '',
                        "describeShop": '',
                        "pinglunTime": '',
                        "pinglun": ''
                    }
                    with open('total_semir_comments_deal.csv', 'a+', newline='', errors='ignore',  encoding='utf-8') as f:
                        f_csv = csv.DictWriter(f, fieldnames=fieldnames)
                        f_csv.writeheader()
                        f_csv.writerow(one_comment_dict)
                    print('没有评论, 跳过')
                else:
                    # 通过总页数，每页访问，获得评论数据
                    for one_page in range(1, commnet_pages + 1):
                        print('{}的第{}页评论正在下载中……'.format(one_city_one_shop_name, one_page))
                        if one_page == 1:
                            # 如果是第一页，不对链接进行操作，如果是后续页面，则加上“/p页数”
                            pass
                        else:
                            review_all_url = one_city_one_shop_url + '/review_all/p{}'.format(one_page)
                            # 访问新的页数,抓取评论
                            shopdriver.get(review_all_url)
                            shopdriver.implicitly_wait(5)
                            time.sleep(3)
                        # 调用pyquery,对网页源码进行解析,参考csdn上大神的思路
                        doc = pq(shopdriver.page_source)
                        # 获取当前页面的字体css和svg数据,并处理成规范格式
                        time.sleep(1)
                        total_lst_dict, dict_css = self.css_get(doc)
                        pinglunLi = list(doc("div.reviews-items > ul > li").items())
                        time.sleep(8)
                        # 通过解密，获得一页评论的所有数据
                        # 针对部分店铺数据计数有两条评论,但是实际上没有评论的问题,在pinglunLi的评论列表中进行判断,如果pinglunLi不为空,继续执行
                        if pinglunLi:
                            for data in pinglunLi:
                                # 用户名
                                userName = data("div.main-review > div.dper-info > a").text()
                                if userName == '':
                                    userName = data("div.main-review > div.dper-info > span").html()
                                # 用户ID链接
                                try:
                                    userID = "http://www.dianping.com" + data("div.main-review > div.dper-info > a").attr("href")
                                # except TypeError:
                                #     userID = "http://www.dianping.com/" + data("div.main-review > div.dper-info > span").html()
                                except:
                                    userID = ''
                                # 用户评分星级[10-50]
                                try:
                                    startShop = str(data("div.review-rank > span").attr("class")).split(" ")[1].replace("sml-str", "")
                                except IndexError:
                                    startShop = ''
                                # 用户描述：机器：非常好 环境：非常好 服务：非常好 人均：0元
                                describeShop = data("div.review-rank > span.score").text()
                                # 关键部分，评论HTML,待处理，评论包含隐藏部分和直接展示部分，默认从隐藏部分获取数据，没有则取默认部分。（查看更多）
                                time.sleep(1)
                                pinglun = self.pinglun_deal(data)
                                #  print(css_decode(total_lst_dict, dict_css, pinglun))
                                # 发表评论的时间
                                pinglunTime = data("div.main-review > div.misc-info.clearfix > span.time").text()
                                one_comment_dict = {
                                    "province_name": province_name,
                                    "city_name": city_name,
                                    "one_city_one_shop_url": one_city_one_shop_url,
                                    "one_city_one_shop_name": one_city_one_shop_name,
                                    "userName": userName,
                                    "userID": userID,
                                    "startShop": startShop,
                                    "describeShop": describeShop,
                                    "pinglunTime": pinglunTime,
                                    "pinglun": self.css_decode(total_lst_dict, dict_css, pinglun)
                                }
                                print('{}: {}'.format(userName, one_comment_dict["pinglun"]))
                                with open('total_semir_comments_deal.csv', 'a+', newline='', errors='ignore', encoding='utf-8') as f:
                                    f_csv = csv.DictWriter(f, fieldnames=fieldnames)
                                    f_csv.writeheader()
                                    f_csv.writerow(one_comment_dict)
                                print('{}的评论下载完成\n'.format(one_city_one_shop_name))
                        else:
                            print('计数上有数据,但实际无数据')
            except exceptions.InvalidSessionIdException:
                print('浏览器已经关闭')
                shopdriver.quit()
                break
            except Exception as e:
                print(e)
                wrong_page = shopdriver.find_elements_by_css_selector('html > body > div.not-found > div.not-found-content > div.not-found-right > p.not-found-words1')
                if wrong_page:
                    print('需要重新登录,更换请求头', one_city_one_shop_url)
                    shopdriver.quit()
                    break
                    # continue
                else:
                    print('出现了错误,请及时处理', one_city_one_shop_url)
                    continue

    def compare_down_data(self):
        not_down_shop_file = []
        with open(r'D:\Python\VisualCode\total_semir_comments_deal.csv', 'r', encoding='utf-8') as f1:
            f_csv1 = csv.reader(f1)
            file_down = list(f_csv1)
        coments_shop_url = [i[2] for i in file_down if i[2] != 'one_city_one_shop_url']
        with open(r"D:\Test\dazhongdianping_semir_address.csv", 'r', encoding='utf-8') as f2:
            total_rows =  csv.reader(f2)
            file_config = list(total_rows)
        config_shop_url = [i[3] for i in file_config]
        not_down_href = list(set(config_shop_url).difference(set(coments_shop_url)))
        for one_href in not_down_href:
            for one_row in file_config:
                if one_href in one_row:
                    not_down_shop_file.append(one_row)
        print('还有{}家等待抓取'.format(len(not_down_shop_file)))
        return not_down_shop_file

    def restart_driver_down(self):
        count = 1
        while True:
            have_data = self.compare_down_data()
            shopdriver = self.start_driver()
            self.dianping_login(shopdriver)
            self.down_one_shop_comments(shopdriver, have_data)
            if count > 10:
                break
            count += 1


if __name__ == "__main__":
    one_comment = DianPingSpider()
    # shopdriver = one_comment.start_driver()
    # one_comment.dianping_login(shopdriver)
    # one_comment.get_total_semir_href(shopdriver)
    one_comment.restart_driver_down()
    # print(one_comment.have_data)