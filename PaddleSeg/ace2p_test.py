#-*-coding:utf-8-*- 
__author__ = 'AeenPython'


import paddlehub as hub

ace2p = hub.Module(name="ace2p")

test_img_path = r"D:\Python\ImageCv\PaddleSeg\contrib\ACE2P\data\1909wuhan\IMG_0827-objectsperson-2.jpg"

# set input dict
input_dict = {"image": [test_img_path]}

# execute predict and print the result
results = ace2p.segmentation(data=input_dict)
for result in results:
    print(result['origin'])
    print(result['processed'])