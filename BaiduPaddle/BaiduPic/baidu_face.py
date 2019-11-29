#!/usr/bin/env python
# coding: utf-8

# In[2]:


import base64
import os
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

    def create_finished_dir(self, picture_path):
        ok_file = '{}\\ok'.format(picture_path)
        del_file = '{}\\del'.format(picture_path)
        try:
            os.makedirs(ok_file)
            print('创建文件夹成功')
        except Exception as e:
            print(e)
            print('文件夹已经存在')
            pass
        try:
            os.makedirs(del_file)
            print('创建文件夹成功')
        except Exception as e:
            print(e)
            print('文件夹已经存在')
            pass
        return ok_file, del_file


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
        ok_file, del_file = self.create_finished_dir(picture_path)
        all_result = []
        all_file_path = Path(picture_path).glob('*.jpg')
        for one_picture in all_file_path:
            if one_picture.is_file():
                print('\t{}正在访问中'.format(one_picture.name))
                base64_data = self.get_base64(one_picture)
                try:
                    one_person_face = self.get_face_gender(base64_data)
                    one_person_face['path'] = '{}\\{}'.format(ok_file, one_picture.name)
                    df = pd.DataFrame(one_person_face,index=[0])
                    df.to_csv('{}\\{}'.format(ok_file, 'result.csv'), mode='a+')
                    all_result.append(one_person_face)
                    one_picture.replace('{}\\{}'.format(ok_file, one_picture.name))
                except (IndexError, TypeError, FileNotFoundError) as e:
                    # print('\t', e)
                    # print(one_picture.name)
                    one_picture.replace('{}\\{}'.format(del_file, one_picture.name))
                except FileNotFoundError as e:
                    pass
                print('\t{}访问结束\n'.format(one_picture.name))
        return '{}已经整理结束'.format(picture_path.as_posix())

    def main(self):
        base_dir = r'D:\内部共享\消费者图库\20190322街拍\segment\补充'
        all_segment_path = Path(base_dir).iterdir()
        for picture_path in all_segment_path:
            print('{}开始整理了'.format(picture_path.as_posix()))
            print(self.one_segment_path(picture_path))
        return '所有的均已完成'

if __name__ == '__main__':
    person = PersonMoreDeal()
    person.main()
