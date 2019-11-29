# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 18:07:50 2018

@author: leshuangjiang
"""
import os
import time

# import re
import pandas as pd
import xlwings as xw


#os.system('taskkill /F /IM EXCEL.exe')
def get_all():       #获取所有的核价单名单和地址
    '''这个函数是进行核价单目录的处理'''
    path = r'D:\核价单汇总\已经核完价的核价单'
    return [os.path.join(path, i) for i in os.listdir(path)]

#def get_fraction():
#    '''这个函数是进行核价单目录的处理'''
#    path = r'D:\核价单汇总\已经核完价的核价单'
#    name_lst = [os.path.join(path, i) for i in os.listdir(path)]
#    xb_res_2 = app.books.open(r'D:\核价单汇总\模板\汇总.xlsx')
#    col = xb_res_2.sheets[0].range('a2:a50000').value
#    xb_res_2.close()
#    coll = [str(int(i)) for i in col if i != None]
#    name_kuanhao = [re.findall(r'\\(\d*\d)', i)[0] for i in name_lst]
#    [name_kuanhao.remove(i) for i in coll if i in name_kuanhao]
#    res_name = [path+'\\'+i+'.xlsx' for i in name_kuanhao]
#    return res_name
#four_c = [df[2].tolist().index(i) for i in choice]
#choice = [面料小计:', '辅料小计:', '工利税', '洗水']
#def getLocation():


def fun_df(name):    #将数据读入到内存中
    '''将数据读入到内存中'''
    rng = name.range('a1:l300').value
    return pd.DataFrame(rng)

def emb_flower():           #获取印绣花的价格
    '''获取印绣花的价格'''
    a = df[2].tolist()
    s = [str(i) for i in a if i != None]
    t = 200
    for j in s:
        if '印' in j:
            t = a.index(j)
        elif '绣' in j:
            t = a.index(j)
        elif '花' in j:
            t = a.index(j)
        else:
            continue
    #    Emb_flower_price = df[9][s]
    return  df[9][t]
#    Emb_flower = df[2][s]


def material():         #获取面料和辅料的总价
    '''获取面料和辅料的总价'''
    try:
        mat_num = df[2].tolist().index('面料小计:')
        acc_num = df[2].tolist().index('辅料小计:')
    except ValueError as e:
#        print(e)

        mat_num = df[2].tolist().index('面料小计')
        acc_num = df[2].tolist().index('辅料小计')
    mat_price = df[9][mat_num]
    acc_price = df[9][acc_num]
    return mat_price, acc_price


def wash():         #获取洗水的总价
    '''获取洗水的总价'''
    try:
        Wash_water_num = df[2].tolist().index('洗水')
        Wash_water = df[9][Wash_water_num]
    except ValueError as e:
        try:
            Wash_water_num = df[2].tolist().index('洗水')
            Wash_water = df[9][Wash_water_num]
        except ValueError as e:
            Wash_water = None
    return Wash_water


def Ind_tax():      #获取工利税
    try:
        IndTax = df[2].tolist().index('工利税')
        Ind_tax_price = df[9][IndTax]
        sew_price = None
        sum_price = df[3][IndTax + 1]
    except ValueError as e:
#        print(e)
        IndTax = df[6].tolist().index('工利税')
        Ind_tax_price = df[9][IndTax]
        sew_price = df[9][IndTax+1]
        sum_price = df[3][IndTax + 2]
    return Ind_tax_price, sum_price, sew_price


def GetData(name):      #获取款号、色号和模式的信息
    style_num = [name.range('h3').value, xb.sheets[name].range('d3').value]
    name_num = [i for i in style_num if len(str(i))>=11 ][0]
    color_num = name.range('i3').value
    model = name.range('k1').value
#   name_style = xb.sheets[0].range('d4').value
    return [name_num, color_num, model]


def getHave():      #获取已有数据的行数
    df_Have = pd.DataFrame(xb_res.sheets[0].range('a1:l50000').value)
    df_Have.dropna(axis=0, how='all', inplace=True)
    return len(df_Have)


def getEmbody():        #汇总操作
    mat_price, acc_price = material()
    Ind_tax_price, sum_price, sew_price = Ind_tax()
    Emb_flower_price = emb_flower()
    wash_flower = wash()
    embody = [mat_price, acc_price, Ind_tax_price, Emb_flower_price, wash_flower, sew_price, sum_price]
    return embody


def drop_dup():     #对数据去重处理
    xb_res_2 = app.books.open(r'D:\核价单汇总\模板\汇总.xlsx')
    col = xb_res_2.sheets[0].range('a1:j1').value
    rng = xb_res_2.sheets[0].range('a2:j50000').value
    xb_res_2.close()
    df_dup = pd.DataFrame(rng, columns=col)
    df_dup.dropna(axis=0, how='all', inplace=True)
    df_dup.replace([None], '', inplace=True)
    df_dup['色号'] = df_dup['色号'].apply(lambda x: '0'+str(x)[:-2] if isinstance(x,float) else x)
    df_dup = df_dup.astype('str')
    df_dup['款号'] = df_dup['款号'].str[:-2]
    df_dup.drop_duplicates(subset=['款号', '色号'], keep='last', inplace=True)
#    os.remove(r'D:\核价单汇总\模板\汇总.xlsx')
    df_dup.to_excel(r'D:\核价单汇总\模板\汇总.xlsx', index=False)
    print('刷新原有数据成功')
    print('数据一共有', len(df_dup))
#    df_dup.to_sql('d:\\备份.db')
    return '数据正在写入， 请等待……'
#os.system('taskkill /F /IM EXCEL.exe')


app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = True
xb_res = app.books.open(r'D:\核价单汇总\模板\汇总.xlsx')
all_location = getHave() + 1
print('原有数据共有', all_location-2, '行')
all_value = []
for i, x in enumerate(get_all()):
    multi_color = []
    try:
        xb = app.books.open(x)
        print(xb.name, '正在写入……')
        need_sheet = [i for i in xb.sheets if i.api.visible==-1 and "齐色" in i.name]
        for i in need_sheet:
            df = fun_df(i)
            title = GetData(i)
            title.extend(getEmbody())
            multi_color.append(title)
        print(xb.name, '已经写入\n')
        xb.close()
        all_value.extend(multi_color)
    except Exception as e:
        print(e)
        print('表格出现临时文件，请刷新……')
        time.sleep(5)
        print('请重新运行本程序……')
        continue

all_location = all_location + len(multi_color)
loc = str(all_location)
xb_res.sheets[0].range(''.join(['a', loc])).value = all_value
app.screen_updating = True
try:
    xb_res.save(r'D:\核价单汇总\模板\汇总.xlsx')
#    time.sleep(5)
    xb_res.close()
    print(drop_dup())
    print('所有的数据均已写入，请查看')
except Exception as e:
    print(e)
    print('wrong')
finally:
    app.quit()
    xw.App.kill(app)
#os.system('taskkill /F /IM EXCEL.exe')

#os.system('taskkill /F /IM EXCEL.exe')
#def main_mat():   #获取主面料的价格
#    try:
#        main_mat_num = df[8].tolist()[:20].index('单价(元)')
#    except ValueError as e:
##        print(e)
#        main_mat_num = df[8].tolist()[:20].index('单价(元）')
#    main_mat_price = df[8][main_mat_num+1]
#    return main_mat_price
#mat_num = df[2].tolist().index('面料小计:')
#acc_num =  df[2].tolist().index('辅料小计:')

#  if len(need_sheet) == 1:
#            df = fun_df(0)
#            title = GetData(0)
#            title.extend(getEmbody())
#            all_location = all_location + 1
#            loc = str(all_location)
#            xb_res.sheets[0].range(''.join(['a', loc])).value = title
#            app.screen_updating = True
