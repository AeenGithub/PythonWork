# coding: utf-8
import os
import re

import pandas as pd

base_dir = r'D:\Test\tmall'
lst_brand = [base_dir + '\\' + i for i in os.listdir(base_dir) if i.endswith('1110')]
all_brand = []
for one_brand in lst_brand:
    print(one_brand)
    file1 = open(one_brand, 'r', encoding='utf-8')
    file = file1.read()
    test = re.compile("'titleUnderIconList'(.*?)'store_name'")
    new_file = test.sub("'store_name'", file)
    last_file = new_file.split(']')[1:-1]
    all_page = []
    for one_page in last_file:
        pages = eval(one_page + ']')
        df = pd.DataFrame(pages)
        all_page.append(df)
    brand = pd.concat(all_page, sort=True)
    brand.to_excel('d:\\test\\brand\\result\\{}.xlsx'.format(one_brand.split('\\')[-1]))
    all_brand.append(brand)
    file1.close()