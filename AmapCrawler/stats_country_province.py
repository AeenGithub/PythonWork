import requests
import time
from bs4 import BeautifulSoup
import lxml
from lxml import etree
import time
import pandas as pd
from retrying import retry

total_counts = 65
init_code = ['{:0>2d}'.format(i) for i in range(11, total_counts + 1)]
init_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html'
init_code = [(i+'.html', init_url) for i in init_code]


stats_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181'
}

@retry(stop_max_attempt_number=5, wait_random_min=100, wait_random_max=2000)
def get_one_class_table(url, one_code_url):
    time.sleep(0.5)
    print(one_code_url, '正在访问中……')
    stats_resp = requests.get(url, headers=stats_headers)
    stats_resp.encoding = 'gbk'
    # print(stats_resp.status_code)
    if stats_resp.status_code == 200:
        # print(stats_resp.text)
        soup = BeautifulSoup(stats_resp.text, 'lxml')
        info_table = soup.select('body > table:nth-child(3) > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tr')
        if not info_table:
            return [[one_code_url, '', '', '', '', url]]
        one_page_lst = []
        for one_row in info_table:
            one_col_lst = []
            for one_col in one_row.select('td'):
                try:
                    one_col_lst.append(one_col.text)
                    one_col_lst.append(one_col.a['href'])
                    print('\t', one_col_lst)
                except (TypeError, AttributeError) as e:
                    print('\t', one_code_url, 'wrong')
                    one_col_lst.append('')
            one_col_lst.insert(0, one_code_url)
            one_col_lst.append(url)
            one_page_lst.append(one_col_lst)
        print(one_code_url, '访问结束了\t')
        return one_page_lst


def total_level_down(init_code, level):
    one_level_lst = []
    for one_code in init_code:
        if one_code:
            one_code_url = one_code[0]
            init_url = one_code[1]
            url_suffix = '/'.join(init_url.split('/')[:-1]) + '/'
            url = url_suffix + one_code_url
            '需要一层重复递归'
            one_page_table = get_one_class_table(url, one_code_url)
            if one_page_table:
                one_level_lst.extend(one_page_table)
    init_code = [(i[2], i[-1]) for i in one_level_lst if i[1].isdigit()]
    df = pd.DataFrame(one_level_lst)
    df.to_excel('行政区划_{}.xlsx'.format(level))
    print('行政区划_第{}页保存成功'.format(level))
    level += 1
    return total_level_down(init_code, level)

level = 1
total_level_down(init_code, level)
