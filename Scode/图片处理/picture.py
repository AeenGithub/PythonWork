# coding: utf-8
from pathlib import Path
p = Path(r'C:\Users\Public\Pictures\Sample Pictures')
l = [i for i in p.iterdir() if i.is_file()]
l
l[0]
title = '"
title = '"
title = '"<table> <img src="'
last = '"width=160 height=120>'
res = [title+i+last for i in l]
l[0]
f = l[0]
str(f)
res = [title+str(i)+last for i in l]
res
title = '<table> <img src="'
res = [title+str(i)+last for i in l]
res
with open(r'd:122.txt, 'w') as f:
with open(r'd:122.txt', 'w') as f:
    for i in res:
        f.write(i)
        
with open(r'd:122.txt', 'w') as f:
    for i in res:
        f.write(i)
        f.write('\n')
        
l
f
l[0]
g = l[0]
g.drive
g.home()
g.parent
g.parents
g.parents()
g.parents
g.name
with open(r'd:\222.txt', 'w') as f:
    for i in l:
        f.write(i.name)
        f.write(title+str(i)+last)
        f.write('\n')
        
with open(r'd:\222.txt', 'w') as f:
    for i in l:
        f.write(i.name)
        f.write('\t')
        f.write(title+str(i)+last)
        f.write('\n')
        
with open(r'd:\222.txt', 'w') as f:
    for i in l:
        f.write(i.name)
        f.write('\t')
        f.write(title+str(i)+last)
        f.write('\n')
        
get_ipython().run_cell_magic('save', 'd:picture n1-n22', '')
get_ipython().run_line_magic('save', 'd:picture n1-n22')
get_ipython().run_line_magic('save', 'd:picture.py n1-n22')
get_ipython().run_line_magic('save', 'd:picture.py 1-36')
p
p[0]
p.iterdir()
for i in p.iterdir():
    i.glob('.jpg')
    
for i in p.iterdir():
    print(i.glob('.jpg'))
    
    
[i for i in p.iterdir() if i.glob('.jpg')]
[i for i in p.iterdir().rglob('.jpg')]
[i for i in p.rglob('.jpg')]
[i for i in p.rglob('*.jpg')]
def lst_tree(p, n):
    if p.is_file():    #判断是否是文件
        print('|' + '\t|' * n + '-' * 4 +  p.name)
    elif p.is_dir():    # 判断是否是目录
        print('|' + '\t|' * n + '-' * 4 +  str(p.relative_to(p.parent)) + '\\')
        for pt in p.iterdir():
            lst_tree(pt, n + 1)   # 递归
            
lst_tree(p)
lst_tree(p,0)
lst_tree(p,1)
lst_tree(p,0)
type(lst_tree(p,0))
lst_tree(p,0)[0]
for i in lst_tree(p,0):
    print(i)
    
