import turtle
import math

# 创建一个画布
t = turtle.Turtle()

# 设置画笔速度（1-10，10最快）
t.speed(5)

# 画大圆
t.circle(100)  # 100是半径，单位为像素

# 画12个小球
radius = 100  # 大圆半径
small_radius = 10  # 小球半径
t.penup()

for i in range(12):
    # 计算每个小球的位置
    angle = math.radians(i * 30)  # 将360度平均分成12份
    x = radius * 0.6 * math.sin(angle)
    y = radius * 0.6 * math.cos(angle)
    
    # 移动到小球位置
    t.goto(x, y - radius)
    
    # 画小球
    t.pendown()
    t.begin_fill()
    t.circle(small_radius)
    t.end_fill()
    t.penup()

# 保持窗口显示
turtle.done()