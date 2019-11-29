import json
import logging

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AiRecognitionTest(object):

    def test_fashionbi_recognition(self):
        gw = 'http://60.190.243.234:8206/fashionbi/recognition'

        url = 'https://zhiyi-image.oss-cn-hangzhou.aliyuncs.com/old_df/instagram/927185_658783480854602_924916565_n.jpg'
        data = {
            'images': [ #识别的图片列表,每个图片为一个json对象，格式如下
                {
                    'union_id': 'unionidxxxx', #唯一标识
                    'platform_id': '0', #平台id，默认0
                    'url': 'https://img.alicdn.com/imgextra/i4/397341302/O1CN01lsPzkr1LUMAoPL9FH-397341302.jpg' #图片可访问的url
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
    test.test_fashionbi_recognition()