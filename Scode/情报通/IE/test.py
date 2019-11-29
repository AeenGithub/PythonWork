import os
import pickle

import pandas as pd


def func_one():
    with open('seniorclss', 'rb') as f:
        df = pickle.loads(f.read())
        df.to_excel('seniorclss.xlsx')

def func_two():
    df_demo = pd.read_clipboard()
    with open('seniorclss', 'wb') as f:
        f.write(pickle.dumps(df_demo))
        print('ok')

func_two()
# func_one()
print(os.getcwd())

