 # -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:43:00 2018

@author: S103878
"""

 import time
 from pathlib import Path


 def filedo():
    p = Path(r'C:\Users\leshuangjiang\Pictures\天猫图库')
    title = '<table>\n'
    title_2 = '<td><img src="file:///'
    last_2 = '" width=80 height=80 /></td></tr>\n'
    last = '</table>\n'
    l = [i for i in p.glob('**/*.jpg') if i.is_file()]
    with open('D:\\Tmall.html', 'w') as f:
        f.write(title)
        for i in l:
            f.write('<tr>\n<td>'+str(i.parent)+'</td>\n')
            f.write('<td>'+i.name[:-4]+'</td>\n')
            f.write('<td>'+time.strftime('%Y-%m-%d', time.localtime(i.stat()[-1]))+'</td>\n')
            f.write(title_2+str(i)+last_2)
        f.write(last)

#def write_file():
#    wb = xw.Book.caller()
#    wb.sheets[0].activate()
#    wb.sheets[0].range('a2').api.select
#    wb.sheets[0].api.paste
#    return 1

# def deal_Clipboard():
#     p = Path(r'E:\\Tmall.html')
#     filedo()
    # wincb.OpenClipboard()
    # wincb.EmptyClipboard()
    # wincb.SetClipboardText(p.read_text())
    # wincb.CloseClipboard()


p = Path(r'D:\\Tmall.html')
filedo()


