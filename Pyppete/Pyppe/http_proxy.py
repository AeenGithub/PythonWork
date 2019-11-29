import json
import os
import pickle
import re
import urllib.parse as uparse

TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.6.8/index.js'
other_url = 'https://g.alicdn.com/secdev/sufei_data/3.6.7/index.js'
INJECT_TEXT = 'Object.defineProperties(navigator,{webdriver:{get:() => undefined}});'
INJECT_TEXT = ""

def response(flow):
    if flow.request.url.startswith(TARGET_URL):
        flow.response.text = INJECT_TEXT + flow.response.text
        print('注入成功')

    if 'um.js' in flow.request.url or '115.js' in flow.request.url:
    # 屏蔽selenium检测
        flow.response.text = flow.response.text + INJECT_TEXT

    if flow.request.url.startswith(TARGET_URL):
        flow.response.text = flow.response.text.replace('$cdc_asdjflasutopfhvcZLmcfl_', '$dog_asdjflasutopfhvcZLmcfl_')
        # print(flow.response.text)

    if 'index.js' in flow.request.url:
        flow.response.text = flow.response.text.replace('$cdc_asdjflasutopfhvcZLmcfl_', '$dog_asdjflasutopfhvcZLmcoo_')
        print('修改成功')

    if 'appsearch' in flow.request.url and 'jsv=2.4.2' in flow.request.url:
        data_url = uparse.unquote(flow.request.url)
        quering_data = json.loads(re.findall(r'{.*?}', data_url)[0])
        shop_id = quering_data['shopId']
        infos = re.findall(r'\(({.*})\)', flow.response.text)[0]
        infos = json.loads(infos)
        if infos.get('data'):
            data = infos.get('data')
            new_one_page = []
            totalResults = data.get('totalResults')
            page = data.get('page')
            totalPage = int(data.get('totalPage'))
            one_page_dict = data.get('itemsArray')
            for one_piece in one_page_dict:
                one_piece['page'] = page
                one_piece['totalPage'] = totalPage
                one_piece['totalResults'] = totalResults
                new_one_page.append(one_piece)
            if not os.path.exists('e:\\mitm\\{}_{}.pkl'.format(shop_id, page)):
                with open('e:\\mitm\\{}_{}.pkl'.format(shop_id, page), 'ab+') as f:
                    f.write(pickle.dumps(new_one_page))
                with open('e:\\mitm\\{}_{}.json'.format(shop_id, page), 'w+', encoding='gbk') as f:
                    f.write(flow.response.text)
            
            

    # document.getElementById("TPL_password_1").value = "17621780176"

    # document.getElementById("TPL_username_1").value = "17621780176"

    # body > div:nth-child(8) > div:nth-child(1) > div > div > div > div > div > div:nth-child(3) > div > span