import json

import requests
from bs4 import BeautifulSoup


class Clothe(object):
    '''clothing'''
    def __init__(self):
        self.url = r'http://b2b.huangye88.com/henan/fuzhuang/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def get_url(self, url):
        init_req = requests.get(url, headers=self.headers)
        init_soup = BeautifulSoup(init_req.text, 'lxml')
        other = init_soup.select('div.box')[2].select('a[href]')
        other = [i.attrs['href'] for i in other]
        return other

    def get_text(self, url):
        num_req = requests.get(url, headers=self.headers)
        num_soup = BeautifulSoup(num_req.text, 'lxml')
        try:
            num = num_soup.select('div.box')[4].select('p')[0].text
        except IndexError:
            num = num_soup.select('div.box')[3].select('p')[0].text
        return num

    def get_all_url(self):
        url_dic = {}
        url_l = self.get_url(self.url)
        # print(len(url_l))
        for url in url_l:
            print(url)
            city = []
            try:
                url_num = self.get_text(url)
            except IndexError:
                url_num = ''
            try:
                one_city = self.get_url(url)
                for one in one_city:
                    try:
                        num = self.get_text(one)
                    except IndexError:
                        num = ''
                    dic_one = {one: num}
                    city.append(dic_one)
                url_dic[url] = {'init_url': url_num, 'city': city}
            except IndexError as e:
                print(e)
                continue
        return url_dic

if __name__ == '__main__':
    clothing = Clothe()
    url_one = clothing.get_all_url()
    with open(r'd:\\clothe3.json', 'w', encoding='utf-8') as f:
        json.dump(url_one, f)
        # f.write(str(url_one))
    print('ok')
