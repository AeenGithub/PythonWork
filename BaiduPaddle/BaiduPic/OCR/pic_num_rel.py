#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

import os

from PIL import Image
from aip import AipOcr


class PicName(object):
    # 编辑图片
    def __init__(self):
        # """ 你的 APPID AK SK """
        APP_ID = '15584553'
        API_KEY = 'MGGfM6EGySBdKOM6605nbhDg'
        SECRET_KEY = 'zxpcnv2pd0VD5zlRwwySFx55BOU0sXhl'
        self.file_path = input('请输入图片文件夹： ')
        self.stylecode = int(input('请输入款号长度： '))
        # self.stylecode = 11
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def get_file_path(self):
        result_file_path = []
        pic_format = ['jpg', 'png']
        try:
            all_file = [os.path.join(self.file_path, i) for i in os.listdir(self.file_path)]
            for i in all_file:
                one_file = os.path.basename(i).lower()
                if '~$' in i:
                    pass
                elif one_file[-3:] in pic_format:
                    result_file_path.append(i)
        except FileNotFoundError as e:
            print('路径输入错误', e)
        return result_file_path

    def get_file_content(self, picture_file):
        img = Image.open(picture_file)
        width, height = img.size
        roi = img.crop((0, 0, width/3*2, height/4))
        # roi.show()
        img.close()
        roi.save('temp.jpg')
        # 读取图片
        with open('temp.jpg', 'rb') as fp:
            return fp.read()

    def get_picture_name(self, picture_file):
        image = self.get_file_content(picture_file)
        # 调用通用文字识别, 图片参数为本地图片
        relative_name = os.path.basename(picture_file)
        dir_name = os.path.dirname(picture_file)
        result_dict = self.client.basicAccurate(image)
        words_result = result_dict['words_result']
        stylecode = words_result[0]['words']
        if len(stylecode) == self.stylecode:
            print('\t{}名称识别成功'.format(relative_name))
        else:
            print('\t{}名称识别不成功'.format(relative_name))
        new_name = os.path.join(dir_name, stylecode+'.jpg')
        os.renames(picture_file, new_name)
        return '\t文件重命名成功'

    def main(self):
         for picture_file in self.get_file_path():
             print(picture_file)
             pic_rename = self.get_picture_name(picture_file)
             print(pic_rename)

if __name__ == '__main__':
    pic_name = PicName()
    pic_name.main()



