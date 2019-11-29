# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:43:00 2018

@author: S103878
"""

import time
from pathlib import Path

import win32clipboard as wincb
import xlwings as xw


def filedo():
    p = Path(r'D:\视频')
    title = '<table>\n'
    title_2 = '<td>file:///'
    last_2 = '" width=160 height=120 /></td></tr>\n'
    last = '</table>\n'
    l = [i for i in p.glob('**/*.MTS') if i.is_file()]
    with open(r'd:\视频.html', 'w') as f:
        f.write(title)
        for i in l:
            f.write('<tr>\n<td>'+str(i.parent)+'</td>\n')
            f.write('<td>'+i.name[:-4]+'</td>\n')
            f.write('<td>'+time.strftime('%Y-%m-%d', time.localtime(i.stat()[-1]))+'</td>\n')
            f.write(title_2+str(i)+'</td>\n')
        f.write(last)
def write_file():
    wb = xw.Book.caller()
    wb.sheets[0].activate()
    wb.sheets[0].range('a2').api.select
    wb.sheets[0].api.paste
    return 1

def deal_Clipboard():
    p = Path(r'd:\视频.html')
    wincb.OpenClipboard()
    wincb.EmptyClipboard()
    wincb.SetClipboardText(p.read_text())
    wincb.CloseClipboard()
    
    

     

