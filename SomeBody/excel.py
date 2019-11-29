# coding: utf-8
import xlwings as xw
app = xw.App(visible=True, add_book=False)
xb = app.books.open(r'C:\Users\leshuangjiang\Desktop\配件.xlsx')
app.screen_updating = False
sht = xb.sheets[0].active
sht = xb.sheets[0]
sht.activate
sht = xb.sheets[1].activate
sht
app.screen_updating = True
lst = sht.range('a1:f25').value
sht = xb.sheets[1]
lst = sht.range('a1:f25').value
lst
for i in lst:
    print(i)
    
for i in lst:
    for y in i:
        print(y)
        
get_ipython().magic('save -f d:\\excel.py 1-17')
