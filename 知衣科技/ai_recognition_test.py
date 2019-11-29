import os
import sys
pdir = os.path.realpath(__file__)
print(sys.path)

import requests
import json
import base64

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AiRecognitionTest(object):

    def test_fashionbi_recognition(self):
        gw = 'http://60.190.243.234:8206/fashionbi/recognition'

        data = {
            'images': [ #识别的图片列表,每个图片为一个json对象，格式如下
                {
                    'union_id': 'unionidxxxx', #唯一标识
                    'platform_id': '0', #平台id，默认0
                    'url': 'https://zhiyi-image.oss-cn-hangzhou.aliyuncs.com/data_infra/9/c11a25203b3430b4600482525d4a6fc9_44a08bf879e33ec3a1eb87a39470f463.jpg' #图片可访问的url
                }
            ]
        }

        try:
            r = requests.post(gw, data=json.dumps(data), timeout=30)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                logger.info('r: {}'.format(json.loads(r.text)))
        except Exception as e:
            logger.error('request fail: {}'.format(e)) 

    def test_fashionbi_recognition_with_payload(self):
        gw = 'http://60.190.243.234:8206/fashionbi/recognition'
        gw = 'http://cpu012:8206/fashionbi/recognition'

        # remote url convert to base64
        url = 'https://zhiyi-image.oss-cn-hangzhou.aliyuncs.com/data_infra/9/c11a25203b3430b4600482525d4a6fc9_44a08bf879e33ec3a1eb87a39470f463.jpg'
        r = requests.get(url, timeout=60)
        base64_content = base64.b64encode(r.content).decode('ascii')

        '''
        # local file convert to base64
        with open(image_path, 'rb') as f:
            content = f.read()
            base64_content = base64.b64encode(content).decode('ascii')
        '''

        data = {
            'images': [ #识别的图片列表,每个图片为一个json对象，格式如下
                {
                    'union_id': 'unionidxxxx', #唯一标识
                    'platform_id': '0', #平台id，默认0
                    'payload': base64_content #图片内容base64编码
                }
            ]
        }

        try:
            r = requests.post(gw, data=json.dumps(data), timeout=30)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                logger.info('r: {}'.format(json.loads(r.text)))
        except Exception as e:
            logger.error('request fail: {}'.format(e))

if __name__ == '__main__':
    test = AiRecognitionTest()
    #test.test_fashionbi_recognition()
    test.test_fashionbi_recognition_with_payload()