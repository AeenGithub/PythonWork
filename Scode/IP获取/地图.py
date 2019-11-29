# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:14:01 2018

@author: S103878
"""

from pyecharts import Map

value = [155, 10, 66, 78]
attr = ["福建", "山东", "北京", "上海"]
map = Map("全国地图示例", width=1200, height=600)
map.add("", attr, value, maptype='china')
map.render()