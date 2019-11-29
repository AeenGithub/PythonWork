import requests

class Yifangyun(object):
    def __init__(self):
        pass

    def get_access_token(self):
        url = "https://oauth.fangcloud.com/oauth/token"
        querystring = {"grant_type":"password","username":"9e117a09c8e069edf6227fd76cf73690","password":"16f30b773304858113036a035639dd9a"}
        payload = ""
        headers = {
            'Authorization': "Basic MzJiNWQzOTYtMzgyYy00ZDc1LTgyNzMtNjU0ZTVlMTcwNDU0OjQ4MjFhOTdmLTg1ZjUtNDM1OC1iYWFkLTkxMmRhZWVhNzUzMg==",
            'cache-control': "no-cache"
            }
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        return response.text

    def get_folder_info(self):
        url = "https://open.fangcloud.com/api/v2/item/search"
        querystring = {"query_words":"1D038000001-6600.jpg","type":"file","query_filter":"file_name"}
        payload = ""
        headers = {
            'Authorization': "Bearer b00cd1d2-f471-4f2a-ae82-c8170c3921e2",
            'cache-control': "no-cache"
            }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        return response.text

    def get_picdown_url(self):
        url = "https://open.fangcloud.com/api/v2/file/521003641219/download"
        payload = ""
        headers = {
            'Authorization': "Bearer b00cd1d2-f471-4f2a-ae82-c8170c3921e2",
            'cache-control': "no-cache"
            }
        response = requests.request("GET", url, data=payload, headers=headers)
        return response.text