#!/usr/bin/env python
# coding: utf-8
import base64
import time
from pathlib import Path

import pandas as pd
from aip import AipFace


class PersonMoreDeal(object):

    def __init__(self):

        """ 你的 APPID AK SK """
        APP_ID = '10207465'
        API_KEY = '6kGyHckLOnH9Y3TuLGbopLG9'
        SECRET_KEY = 'OReYFNrB9BB5eh0kwgj2OEssxe0aTROl'
        self.client = AipFace(APP_ID, API_KEY, SECRET_KEY)
        self.url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

    def get_base64(self, one_picture):
        """对照片进行处理，进行base64编码"""
        if one_picture.is_file():
            base64_data = base64.b64encode(one_picture.read_bytes())
            return base64_data

    def get_face_gender(self, base64_data):
        """利用baidu接口进行人脸和性别检测"""
        imageType = "BASE64"
        options = {}
        options["face_field"] = "age,gender,race,quality,beauty"
        options["max_face_num"] = 2
        options["face_type"] = "LIVE"

        """ 带参数调用人脸检测 """
        json_data = self.client.detect(base64_data.decode(), imageType, options)
        time.sleep(0.1)
        if json_data.get('result', 0) and json_data['result']['face_list']:
            age = json_data['result']['face_list'][0]['age']
            gender = json_data['result']['face_list'][0]['gender']['type']
            facequality = json_data['result']['face_list'][0]['beauty']
            face_probability = json_data['result']['face_list'][0]['face_probability']
            blurness = json_data['result']['face_list'][0]['quality']['blur']
            blurness_threshold = json_data['result']['face_list'][0]['quality']['completeness']
            last_result = {
                'gender': gender,
                'age': age,
                'facequality': facequality,
                'face_probability': face_probability,
                'blurness': blurness,
                'blurness_threshold': blurness_threshold
            }
            return last_result

    def one_segment_path(self, picture_path):
        all_result = []
        all_file_path = Path(picture_path).glob('**/*.jpg')
        one_picture_res = time.strftime("%y%m%d%H%M%S")
        for one_picture in all_file_path:
            if one_picture.is_file() and '女' in one_picture.as_posix() or '男' in  one_picture.as_posix():
                print('\t{}正在访问中'.format(one_picture.name))
                base64_data = self.get_base64(one_picture)
                try:
                    one_person_face = self.get_face_gender(base64_data)
                    one_person_face['path'] = one_picture.as_posix()
                    df = pd.DataFrame(one_person_face, index=[0])
                    df.to_csv('{}\\{}{}.csv'.format(picture_path.parent, one_picture.parent.parent.parent.name, one_picture_res), mode='a+')
                    all_result.append(one_person_face)
                except (IndexError, TypeError, FileNotFoundError) as e:
                    print('\t', e)
                    print(one_picture.name)
                except FileNotFoundError as e:
                    pass
                print('\t{}访问结束\n'.format(one_picture.name))
        return '{}已经整理结束'.format(picture_path.as_posix())

    def main(self):
        base_dir = r'D:\内部共享\消费者图库\20190322街拍\segment'
        all_segment_path = Path(base_dir).iterdir()
        for picture_path in all_segment_path:
            print('{}开始整理了'.format(picture_path.as_posix()))
            print(self.one_segment_path(picture_path))
        return '所有的均已完成'


if __name__ == '__main__':
    person = PersonMoreDeal()
    person.main()
