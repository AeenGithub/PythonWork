
# coding: utf-8

import re
from collections import OrderedDict

import jieba
import pandas as pd


class ItemID(object):
    def __init__(self):
        jieba.load_userdict("./PailitaoCrawler/temp/clothe_dict")
        pattern = r'T|恤|裤|克|帽|盒|包|带|结|巾|棒|罩|雨|手机|心|袍|唐|靴|镜|挂|枕|利领|床|环|杯|高腰|圆领|条纹短|拖|袜|袖|鞋|裙|夹|群|连衣|配|饰'
        self.clothe_class = re.compile(pattern, re.I)
        self.patt_jeans = re.compile(r'牛仔', re.I)

    def niuzai(self, col):
        if '牛仔' in col:
            if '短裤' in col:
                col.append('牛仔短裤')
            elif '长裤' in col:
                col.append('牛仔长裤')
            elif '连体裤' in col:
                col.append('牛仔连体裤')
            elif '中裤' in col:
                col.append('牛仔中裤')
            elif '休闲' in col:
                if '外套' in col:
                    col.append('外套')
                else:
                    col.append('牛仔长裤')
            else:
                col.append('牛仔裤')
        return col

    def deal_title(self, df):
        """对传入的dataframe数据进行处理"""
        df['小类'] = ''
        df['中类'] = ''
        df['大类'] = ''
        df['title'] = df['title'].str.replace('【商场同款】', '')
        df['title'] = df['title'].str.replace('群', '裙')
        df['title'] = df['title'].str.replace('体恤', 'T恤')
        df['jieba'] = df['title'].apply(lambda x: list(jieba.posseg.cut(x)))
        df['jeans'] = (df['title'].apply(lambda x: self.patt_jeans.findall(x)))
        df['title简称'] = (df['jieba'].apply(lambda x: [i.word for i in x if i.flag == 'nz' or i.flag == 'ng'])
                         .apply(lambda x: self.niuzai(x))
                         .apply(lambda x: set(x))
                         .apply(lambda x: [i.replace('体恤', 'T恤') for i in set(x)])
                         .apply(lambda x: [i for i in x if x != ' ' and i.isalpha()])
                         .apply(lambda x: '|'.join(set(x))))
        df['名词'] = (df['jieba'].apply(lambda x: [i.word for i in x if i.flag == 'n'])
                    .apply(lambda x: set(x))
                    .apply(lambda x: [i.replace('体恤', 'T恤') for i in set(x)])
                    .apply(lambda x: [i for i in x if x != ' ' and i.isalpha()])
                    .apply(lambda x: '|'.join(set(x))))
        # 对于字典中不存在的小类,采用具有名词属性的词来标注
        rep_val = df.loc[df.index[(df['title简称'] == '')], ['名词']].values
        df.loc[df.index[(df['title简称'] == '')], ['title简称']] = rep_val
        mid_rank = []
        df['hat_shoes_2'] = ''
        df['hat_shoes'] = (df['title'].apply(lambda x: self.clothe_class.findall(x))
                           .apply(lambda x: ''.join(set(x))))
        with open("./PailitaoCrawler/temp/rule_of_rank", encoding='utf-8') as f:
            skirts = f.read().split('\n')
        mid_rank_dict = OrderedDict()
        mid_rank_dict_2 = OrderedDict()
        mid_rank_dict_3 = OrderedDict()
        for one_rank in skirts:
            mid_rank.append(one_rank.split('\t'))
            mid_rank_dict[one_rank.split('\t')[0]] = one_rank.split('\t')[1]
            mid_rank_dict_2[one_rank.split('\t')[1]] = one_rank.split('\t')[2]
            mid_rank_dict_3[one_rank.split('\t')[2]] = one_rank.split('\t')[3]
        for one_key in mid_rank:
            tmall = one_key[0]
            res = one_key[1]
            df.loc[(df['title简称'].str.find(tmall) != -1), ['小类']] = res
            df.loc[df.index[(df['hat_shoes'].str.find(
                tmall) != -1)], ['hat_shoes_2']] = res
        patt_val = df.loc[df.index[(df['小类'] == '')], ['hat_shoes_2']].values
        df.loc[df.index[(df['小类'] == '')], ['小类']] = patt_val
        df['中类'] = df['小类'].map(mid_rank_dict_2)
        rep_val = df.loc[df.index[(df['小类'] == '')], ['名词']].values
        df.loc[df.index[(df['小类'] == '')], ['title简称']] = rep_val
        df['大类'] = df['中类'].map(mid_rank_dict_3)
        df.drop(['hat_shoes_2', 'hat_shoes', '名词',
                 'title简称', 'jeans', 'jieba', 'title'], axis=1, inplace=True)
        df.to_csv('结果.csv')

    def main(self):
        df = pd.read_clipboard()
        self.deal_title(df)
        return 'ok'


if __name__ == '__main__':
    title = ItemID()
    title.main()
