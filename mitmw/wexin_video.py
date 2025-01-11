from mitmproxy import http


def request(flow: http.HTTPFlow):
    print("request.flow.id:", flow.id)
    request_list = flow.request  # 获取请求对象
    print(request_list.url)


def response(flow: http.HTTPFlow):
    print("response.flow.id:", flow.id)  # 每个请求和响应的flow.id是对应的，同样也是唯一的
    responses_list = flow.response  # 获取响应对象
    print(responses_list.status_code)


