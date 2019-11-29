
# coding: utf-8

# In[1]:


import csv
import re
from collections import OrderedDict

import jieba
import pandas as pd

# In[130]:


all_lst = []
with open(r"D:\Python\QinBaot\test.csv", 'r', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        all_lst.append(row)


# In[131]:


# df = pd.read_excel(r"D:\文档\天猫\ME&CITY折扣服装.xls")


# In[132]:


df = pd.DataFrame(all_lst)
df.rename(columns={'标题': 'title', '名称':'store_name'}, inplace=True)
df.columns


# In[133]:


df['title'] = df['title'].str.upper()


# In[134]:


df = df[(df['title'].str.find('婴儿') == -1) & (df['title'].str.find('童') == -1) & (~df['title'].str.isdigit())]
df = df[(df['title'].str.find('1元入会') == -1) & (df['title'].str.find('太平鸟A') == -1)]


# In[135]:


df['title'] = df['title'].str.replace('【商场同款】', '')
df['title'] = df['title'].str.replace('群', '裙')
df['title'] = df['title'].str.replace('体恤', 'T恤')


# ### 筛选后赋值

# In[136]:


# df['title'] = df['title'] .str.extract(brand_shop, expand=False)[2]
# df['title']
# df['none_brand_title'] = df['title'].str.extract(brand_shop, expand=True)[1]
# df[df['none_brand_title'].isnull()][['none_brand_title','store_name', 'title']]
# df.loc[df.index[df['none_brand_title'].isnull()], ['none_brand_title']] = df.loc[df.index[df['none_brand_title'].isnull()], ['title']].values
# df.loc[df.index[df['none_brand_title'] == ''], ['none_brand_title']] = df.loc[df.index[df['none_brand_title'] == ''], ['title']].values
# df.loc[df.index[df['none_brand_title'].str.count('') < 10], ['none_brand_title']] = df.loc[df.index[df['none_brand_title'].str.count('') < 10], ['title']].values


# ### 建立新的列

# In[137]:


df['小类'] = ''
df['中类'] = ''
df['大类'] = ''


# In[138]:


# df['title_rank'] = df['none_brand_title'].apply(lambda x: list(jieba.cut(x)))


# In[139]:


# 
# df['title_rank'][1689]


# #### 词性分组

# In[182]:


# import pyhanlp
jieba.load_userdict(r"D:\文档\天猫\clothe_dict")


# In[183]:


# df[df['title简称'].str.find('牛仔') != -1]['title简称']
df['jieba'] = df['title'].apply(lambda x: list(jieba.posseg.cut(x)))


# In[185]:


patt_jeans = re.compile(r'牛仔', re.I)
df['jeans'] = (df['title'].apply(lambda x: patt_jeans.findall(x))
                          .apply(lambda x: x[0] if x else ''))


# In[186]:


df['jeans'].value_counts()


# In[187]:


# condition = df['jieba'].apply(lambda x: [i.word for i in x if i.flag == 'n' or i.flag == 'nr'])


# In[188]:


def niuzai(lo):
    if '牛仔' in lo:
        if '短裤' in lo:
            lo.append('牛仔短裤')
        elif '长裤' in lo:
            lo.append('牛仔长裤')
        elif '连体裤' in lo:
            lo.append('牛仔连体裤')
        elif '中裤' in lo:
            lo.append('牛仔中裤')
        elif '休闲' in lo:
            if '外套' in lo:
                lo.append('外套')
            else:
                lo.append('牛仔长裤')
        else:
            lo.append('牛仔裤')
    return lo


# In[189]:


df['title简称'] = (df['jieba'] .apply(lambda x: [i.word for i in x if i.flag == 'nz' or i.flag == 'ng'])
                              .apply(lambda x: niuzai(x))  
                              .apply(lambda x: set(x))
                              .apply(lambda x: [i.replace('体恤', 'T恤') for i in set(x)])
                              .apply(lambda x: [i for i in x if x != ' ' and i.isalpha()])
                              .apply(lambda x: '|'.join(set(x))))


# In[190]:


df['名词'] = (df['jieba'].apply(lambda x: [i.word for i in x if i.flag == 'n'])
                        .apply(lambda x: set(x))
                        .apply(lambda x: [i.replace('体恤', 'T恤') for i in set(x)])
                        .apply(lambda x: [i for i in x if x != ' ' and i.isalpha()])
                        .apply(lambda x: '|'.join(set(x))))


# In[191]:


rep_val = df.loc[df.index[(df['title简称'] == '')], ['名词']].values
df.loc[df.index[(df['title简称'] == '')], ['title简称']] = rep_val


# In[192]:


df.loc[(df['title简称'] == ''), ['title简称', 'title', '名词', 'jieba']]


# In[193]:


# df['jieba'][10701]
# rep_val


# In[194]:


df['jieba'][38069]


# #### 导入匹配规则表

# In[195]:


mid_rank = []
mid_rank_dict = OrderedDict()
mid_rank_dict_2 = OrderedDict()
mid_rank_dict_3 = OrderedDict()
with open(r"D:\Python\QinBaot\rule_of_rank", encoding='utf-8') as f:
    skirts = f.read().split('\n')
for one_rank in skirts:
    mid_rank.append(one_rank.split('\t'))
    mid_rank_dict[one_rank.split('\t')[0]] = one_rank.split('\t')[1]
    mid_rank_dict_2[one_rank.split('\t')[1]] = one_rank.split('\t')[2]
    mid_rank_dict_3[one_rank.split('\t')[2]] = one_rank.split('\t')[3]


# In[196]:


for one_key in mid_rank:
    tmall = one_key[0]
    res = one_key[1]
    df.loc[(df['title简称'].str.find(tmall) != -1), ['小类']] = res


# #### 用正则对帽子-鞋配进行单独处理

# In[198]:


pattern = r'T|恤|裤|克|帽|盒|包|带|结|巾|棒|罩|雨|手机|心|袍|唐|靴|镜|挂|枕|利领|床|环|杯|高腰|圆领|条纹短|拖|袜|袖|鞋|裙|夹|群|连衣|配|饰'     
clothe_class = re.compile(pattern, re.I)
df['hat_shoes'] = (df['title'].apply(lambda x: clothe_class.findall(x))
                              .apply(lambda x: ''.join(set(x))))


# In[199]:


df['hat_shoes_2'] = ''


# In[200]:


for one_key in mid_rank:
    tmall = one_key[0]
    res = one_key[1]
    df.loc[df.index[(df['hat_shoes'].str.find(tmall) != -1)], ['hat_shoes_2']] = res


# In[201]:


# df.loc[(df['hat_shoes_2'].str.find(tmall) == -1), ['hat_shoes_2']]['hat_shoes_2'].value_counts()
# df['小类'].value_counts()


# In[202]:


patt_val = df.loc[df.index[(df['小类'] == '')], ['hat_shoes_2']].values
df.loc[df.index[(df['小类'] == '')], ['小类']] = patt_val


# In[203]:


# df.loc[(df['小类'] == ''), ['title', '小类', 'jieba', 'hat_shoes']]
# df.loc[df.index[(df['小类'] == '')], 'hat_shoes_2'].value_counts()
# df.loc[df.index[(df['小类'] == '')], ['小类']]


# #### 生成中类和大类明细

# In[204]:


# for one_key in mid_rank:
#     mid_res = one_key[1]
#     final_res = one_key[2]
#     df.loc[(df['中类'].str.find(mid_res) != -1), ['小类']] = final_res
df['中类'] = df['小类'].map(mid_rank_dict_2)


# In[205]:


rep_val = df.loc[df.index[(df['小类'] == '')], ['名词']].values
df.loc[df.index[(df['小类'] == '')], ['title简称']] = rep_val


# In[206]:


# df.loc[df.index[(df['小类'] == '')], ['title']]


# In[207]:


# for one_key in mid_rank:
#     mid_res = one_key[2]
#     final_res = one_key[3]
#     df.loc[(df['中类'].str.find(mid_res) != -1), ['大类']] = final_res
df['大类'] = df['中类'].map(mid_rank_dict_3)


# In[208]:


sex_patt = re.compile(r'男女|男女同款|男|女')
quarter_patt = re.compile(r'春|夏|秋|冬|夏秋')


# In[209]:


df['性别'] = (df['title'].apply(lambda x: sex_patt.findall(x))
#                                 .apply(lambda x: set(x))
                                .apply(lambda x: '|'.join(set(x)))
                                .replace('男|男女', '男女')
                                .replace('男|女', '男女'))
df['季节'] = (df['title'].apply(lambda x: quarter_patt.findall(x))
                                .apply(lambda x: set(x))
                                .apply(lambda x: '|'.join(set(x))))
# df['性别'].replace('男|男女', '男女', inplace=True)


# #### 查看性别已经匹配成功的行

# In[210]:


# df[((df['性别'] != '女') & (df['性别'] != '男') & (df['性别'] != ''))][['store_name', '性别', 'title']]
df['性别'].value_counts()
# df[(df['性别'] == '')][['store_name', '性别', 'title']]


# #### 对性别进行品牌匹配

# In[218]:


with open(r"D:\文档\天猫\brand_sex") as f:
    brand_sex_lst = [i.split('\t') for i in f.read().split('\n')]
brand_sex = dict(brand_sex_lst)


# In[212]:


df['性别2'] = df['store_name'].map(brand_sex)
condition = ((df['性别'] != '女') & (df['性别'] != '男') & (df['性别'] != '男女'))
# condition


# In[213]:


df.loc[df.index[condition], ['性别']] = df.loc[df.index[condition], ['性别2']].values


# In[214]:


condition_2 = ((df['性别'] == '') & (df['中类'] == '鞋配'))
df.loc[df.index[condition_2], ['性别']] = '男女'
df.loc[df.index[((df['性别'] == '') & (df['中类'].str.find('裙') != -1))], ['性别']] = '男女'
# df.loc[df.index[df['性别'] == ''], ['store_name', 'title']]
df['性别'].value_counts()


# In[215]:


df.columns


# #### 保存最终结果

# In[216]:


# df[['分类', 'title简称']]
# df[df['分类'] == '']['title简称']
new = df[['store_name', 'sold', 'title', '小类', '中类', '大类', 'title简称', '性别']]
# new = df.drop(['性别2', 'jieba', '名词', 'none_brand_title'], axis=1)
new.to_excel('d:\\3结果.xlsx')


# In[217]:


# for one_item in df['none_brand_title']:
# #     string = '.'.join(one_item)
#     print(one_item)
#     print(clothe_class.findall(one_item))


# In[ ]:


# df.loc[(df['title简称'].apply(lambda x: '衫' in x)) & (df['分类'] == '')][['title', '分类']]
# df.loc[(df['title简称'].apply(lambda x: '克' in x)) & (df['分类'] == '')][['title','title简称']]


# In[ ]:


# clo_patt = re.compile(patt, re.I)


# In[ ]:


# df[df['分类'] != '']['分类']


# In[ ]:


brand_shop = r'(太平鸟|麦檬|MG小象|Material girl|me&city女装|me&city男装|美特斯邦威|npc|欧时力|ONLY|太平鸟女装|Aself|trendiano|优衣库|UR|VEROMODA|viishow|播|clot|速写|伊芙丽|lily|GU|GXG|gxgjeans|韩都衣舍|海澜之家|茵曼|杰克琼斯|JNBY|江南布衣|jucyjudy|kikc|kon|阔色|拉夏贝尔|lilbetter|Lilbetter|Libetter|LILBETTER|毛菇小象|Libette|MG|mg|MECITY|ASELF|TRENDIANO|Vero Moda|VIISHOW|gxg|HSPM|LB)(.*)'


# In[ ]:


pattern = r'O型裤|POLO|T恤|八分裤|包|保温杯|背带裤|背心|背心吊带|编织衫|便服|便裤|便西|踩脚裤|超短裤|衬衫|衬衣|床单|打底裤|打底衫|大衣|道袍|灯笼裤|低裆跨裤|吊带|短裤|短款裤装|短外套|短卫裤|短袖恤|耳环|耳饰|帆布|飞鼠裤|风衣|福袋|格子衫|工装裤|挂绳|哈伦裤|合体喇叭裤|护照夹|加绒裤|家居服|家居裤|夹克|紧身裤|颈链|九分裤|开衫|口罩|裤口褶边|裤子|垮裤|阔脚裤|阔腿|喇叭裤|蕾丝衫|礼服|连体|连体短裤|连体裤|裙|连衣裤|领带|领结|六分裤|萝卜裤|马夹|马甲|慢跑裤|毛巾|毛衫|毛衣|毛针织衫|帽|棉服|棉裤|棉褛|棉衣|抹胸|内裤|牛仔裤|皮带|皮衣|拼条裤|七分裤|铅笔裤|钱夹|茄克|晴雨伞|绒衫|沙滩裤|上衣|上装|手机|手链|束脚|束腿裤|双裤腰|睡裤|睡袍|睡衣|碎花衫|锁骨|唐装|套衫|套头衫|套装|体恤|条纹裤|头带|袜|外套|微喇叭裤|微喇加长裤|微喇裤|围巾|卫裤|卫衣|文胸|五分裤|西服|西服套装|西裤|西装|西装裤|线衫|项链|小脚|小脚长裤|小衫|鞋|胸针|休闲裤|修身裤装|靴|雪纺衫|腰带|腰封|荧光棒|羽绒服|雨衣|浴巾|圆领|运动|运动裤|运动衫|长裤|长款裤装|长卫裤|褶皱裤|针织裤|针织衫|正装裤|直筒|中裤|锥裤|锥形裤|拉链时尚高腰|棒球服|条纹短|底裤|内衣|镜|领巾|袋|挂件|抱枕|裤|宽腿裤|起居裤|蝴蝶衣|长衫|护腿|毯子|手套|护颈|围脖|连身裤|挂饰|扎脚裤|绑结腿裤|雪纺衬|女裤|披肩|摆件|恤|衬|夹|休闲|窄口裤|罩衫|牛仔|松紧裤|起居|手环|发带|拖|衫|花式裤|利领|西|冰袖|喇叭袖|瘦腿裤|长袖中长款|巾|半身群|围|T|荷叶边|露肩|套|休闲长裤|连衣裙|休闲短裤|休闲中裤|牛仔短裤|牛仔长裤|牛仔中裤'


# In[ ]:


# analyse.extract_tags()
# analyse.extract_tags()


# In[ ]:


pants_rank = {}
with open(r"D:\文档\天猫\pants") as f:
    pants = f.read().split('\n')
for one_rank in pants:
    pants_rank[one_rank] = '裤子'


# In[ ]:


pattern_2 = r'O型裤|POLO|T恤|八分裤|包|保温杯|背带裤|背心|背心吊带|编织衫|便服|便裤|便西|踩脚裤|超短裤|衬衫|衬衣|床单|打底裤|打底衫|大衣|道袍|灯笼裤|低裆跨裤|吊带|短裤|短款裤装|短外套|短卫裤|短袖恤|耳环|耳饰|帆布|飞鼠裤|风衣|福袋|格子衫|工装裤|挂绳|哈伦裤|合体喇叭裤|护照夹|加绒裤|家居服|家居裤|夹克|紧身裤|颈链|九分裤|开衫|口罩|裤口褶边|裤子|垮裤|阔脚裤|阔腿|喇叭裤|蕾丝衫|礼服|连体|连体短裤|连体裤|裙|连衣裤|领带|领结|六分裤|萝卜裤|马夹|马甲|慢跑裤|毛巾|毛衫|毛衣|毛针织衫|帽|棉服|棉裤|棉褛|棉衣|抹胸|内裤|牛仔裤|皮带|皮衣|拼条裤|七分裤|铅笔裤|钱夹|茄克|晴雨伞|绒衫|沙滩裤|上衣|上装|手机|手链|束脚|束腿裤|双裤腰|睡裤|睡袍|睡衣|碎花衫|锁骨|唐装|套衫|套头衫|套装|体恤|条纹裤|头带|袜|外套|微喇叭裤|微喇加长裤|微喇裤|围巾|卫裤|卫衣|文胸|五分裤|西服|西服套装|西裤|西装|西装裤|线衫|项链|小脚|小脚长裤|小衫|鞋|胸针|休闲裤|修身裤装|靴|雪纺衫|腰带|腰封|荧光棒|羽绒服|雨衣|浴巾|圆领|运动|运动裤|运动衫|长裤|长款裤装|长卫裤|褶皱裤|针织裤|针织衫|正装裤|直筒|中裤|锥裤|锥形裤|拉链时尚高腰|棒球服|条纹短|底裤|内衣|镜|领巾|袋|挂件|抱枕|裤|宽腿裤|起居裤|蝴蝶衣|长衫|护腿|毯子|手套|护颈|围脖|连身裤|挂饰|扎脚裤|绑结腿裤|雪纺衬|女裤|披肩|摆件|恤|衬|夹|窄口裤|罩衫|牛仔|松紧裤|起居|手环|发带|拖|衫|花式裤|利领|西|冰袖|喇叭袖|瘦腿裤|长袖中长款|巾|半身群|围|T|荷叶边|露肩|套'


# In[ ]:


dfff = pd.DataFrame(pattern_2.split('|'))


# In[ ]:


dfff.to_excel('d:\\fenlei.xls')


# In[ ]:


lo


# In[ ]:


# 


# In[ ]:


# s.isin(['婴儿'])


# In[ ]:


# s[s]


# In[ ]:


p = r'A字裙|O型裤|POLO|T恤|八分裤|百褶裙|半裙|半身裙|包|包臀裙|保温杯|背带裤|背带裙|背心|背心吊带|编织衫|便服|便裤|便西|不规则裙|踩脚裤|超短裤|超短裙|衬衫|衬衣|床单|打底裤|打底衫|大衣|蛋糕裙|道袍|灯笼裤|灯笼裙|低裆跨裤|吊带|短裤|短款裤装|短裙|短外套|短卫裤|短袖恤|耳环|耳饰|帆布|飞鼠裤|风衣|福袋|高腰裙|格子衫|工装裤|公主裙|挂绳|哈伦裤|合体喇叭裤|荷叶边裙|护照夹|花苞裙|及膝裙|加绒裤|家居服|家居裤|夹克|紧身裤|颈链|九分裤|开衫|口罩|裤口褶边|裤子|垮裤|阔脚裤|阔腿|喇叭裤|蕾丝衫|礼服|连身裙|连体|连体短裤|连体裤|连衣|连衣裤|连衣裙|领带|领结|六分裤|萝卜裤|马夹|马甲|慢跑裤|毛巾|毛衫|毛衣|毛针织衫|帽|棉服|棉裤|棉褛|棉衣|抹胸|内裤|牛仔裤|牛仔裙|蓬蓬裙|皮带|皮衣|拼条裤|七分裤|七分裙|铅笔裤|铅笔裙|钱夹|茄克|晴雨伞|裙裤|绒衫|伞裙|沙滩裤|纱裙|上衣|上装|手机|手链|束脚|束腿裤|双裤腰|睡裤|睡袍|睡衣|碎花衫|锁骨|唐装|套裙|套衫|套头衫|套装|体恤|条纹裤|头带|袜|外套|微喇叭裤|微喇加长裤|微喇裤|围巾|卫裤|卫衣|文胸|五分裤|五分裙|西服|西服套装|西裤|西装|西装裤|西装裙|仙女裙|线衫|项链|小黑裙|小脚|小脚长裤|小衫|鞋|胸针|休闲裤|修身裤装|靴|雪纺衫|腰带|腰封|一步裙|荧光棒|羽绒服|雨衣|浴巾|圆领|运动黑色韩版裤|运动裤|运动衫|长裤|长款裤装|长裙|长筒裙|长卫裤|褶皱裤|针织裤|针织衫|正装裤|直筒|直筒裤|直筒裤装|直筒长裤|中裤|中裙|中长裙|锥裤|锥形裤|拉链时尚高腰|棒球服|鱼尾裙|透视裙|条纹短|底裤|内衣|镜|领巾|袋|挂件|碎花裙|抱枕|太平鸟A|休闲男裤|绣花裙|大摆裙|宽腿裤|起居裤|迷你裙|蕾丝裙|窄身裙|喇叭裙|打褶裙|排扣裙|紧身裙|罗纹裙|弹力裙|蝴蝶衣|裙子|长衫|护腿|毯子|手套|护颈|围脖|连身裤|挂饰|扎脚裤|绑结腿裤|雪纺衬|女裤|披肩|摆件|T|衬|夹|窄口裤|睡裙|罩衫|牛仔|松紧裤|起居|手环|发带|拖|衫|花式裤|利领|西|冰袖|喇叭袖|瘦腿裤|腰裙|长袖中长款|丝巾|半身群|针织裙|围领|雪纺裙'


# In[ ]:


pf = pd.DataFrame(p.split('|'))


# In[ ]:


pf.to_excel(r'd:\\fenlei2.xls')


# In[ ]:


k = 'sd4'
k.isalpha()


# In[ ]:


l = [[2,4,5]]
l


# In[ ]:


[i for i in l]

