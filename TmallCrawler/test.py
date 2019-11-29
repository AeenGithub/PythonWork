import requests

url = "https://eichitoo.tmall.com/i/asynSearch.htm"

querystring = {"_ksTS":"1543547307442_116","callback":"jsonp117","mid":"w-15347103346-0","wid":"15347103346","path":"/category.htm","spm":"a1z10.1-b-s.w5001-15882506876.6.d1f512ectGgUZp","search":"y","orderType":"hotsell_desc","scene":"taobao_shop"}

payload = ""
headers = {
    'accept': "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cookie': "cna=E4eHFDtZ31ECAbStZ7GboO4Z; t=20f664e39d4324d8da690212bb21b619; _tb_token_=75335eefebe98; cookie2=1c61d61cf65020cd60b6f2c3e7aac6a3; hng=""; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; whl=-1%260%260%260; cq=ccp%3D0; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=VT5L2FSpccLuJBreK%2BBd&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTYNc5wSzeSlw%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByR1X6Csh5Y3XlQo%3D&id2=Uoe8iq%2F1cXOw4g%3D%3D&nk2=1CAm%2BTqNx%2FMopg%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D; tracknick=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; _l_g_=Ug%3D%3D; ck1=""; unb=1680414312; lgc=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; cookie1=WqH147gwEXHRwypXeqGsjnXlh76p%2FuypS0xDeyQ14Fs%3D; login=true; cookie17=Uoe8iq%2F1cXOw4g%3D%3D; _nk_=%5Cu98CE%5Cu4E91%5Cu51B3%5Cu5730%5Cu8D77; uss=""; csg=450f6992; skt=68a1c73f06902c6d; isg=BDs7xg1u40KT-d_2hdn5AGvpyh-vwEG1LUYQLS34BTpRjFtutWAO4gTOomxnrKeK",
    'referer': "https://eichitoo.tmall.com/category.htm?spm=a1z10.1-b-s.w5001-15882506876.6.d1f512ectGgUZp&search=y&orderType=hotsell_desc&scene=taobao_shop",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "b8e4939b-e5f2-4c41-9b28-6909bb9145bf"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring, allow_redirects=False)

print(response.text)