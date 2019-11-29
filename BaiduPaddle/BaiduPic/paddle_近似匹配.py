#!/usr/bin/env python
# coding: utf-8

# In[5]:


import time

import paddlehub as hub
import pandas as pd

new_table = pd.read_clipboard()

simnet_bow = hub.Module(name="simnet_bow")

table = new_table.copy()


def similarity(x, y):
    inputs = {"text_1": [x], "text_2": [y]}
    try:
        results = simnet_bow.similarity(data=inputs)
    except:
        results = [{'text_1': '', 'text_2': '', 'similarity': 0}]
    return results

total_results = []
for x in table['评语分词'][:1]:
    for y in table['评语分词']:
        print(x, '-->', y)
        one = similarity(x, y)
        time.sleep(0.1)
        total_results.extend(one)

total_df = pd.DataFrame(total_results)

total_df.to_pickle('d:\\test\\近似匹配.pickle')
