TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.6.8/index.js'
other_url = 'https://g.alicdn.com/secdev/sufei_data/3.6.7/index.js'

INJECT_TEXT = 'Object.defineProperties(navigator,{ webdriver:{get:() => undefined}});'
# undefined

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

    if '.js' in flow.request.url:
        flow.response.text = flow.response.text + INJECT_TEXT

    # document.getElementById("TPL_password_1").value = "17621780176"

    # document.getElementById("TPL_username_1").value = "17621780176"