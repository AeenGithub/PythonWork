import re
import requests
import json

a = '''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('e 9(){2 6=4;2 5=\'a\';2 7="g://j.h.f/1/b/4";2 3=["/c.8","/k.8"];o(2 i=0;i<3.l;i++){3[i]=7+3[i]+\'?6=4&5=a&m=\'}n 3}2 d;d=9();',25,25,'||var|pvalue|7261|key|cid|pix|jpg|dm5imagefun|0180361120d67f2b707ed2b6ef983e73|38|3_9536||function|com|https|mangabz||image|4_4189|length|uk|return|for'.split('|'),0,{}))'''

class CartoonCrawler(object):

    def __init__(self):
        self.url = ''
        self.data = ''

    def cartoon(self):
        pattern = '25,25,(.*).split.*'
        test = re.findall(pattern, a)
        print(test[0])
