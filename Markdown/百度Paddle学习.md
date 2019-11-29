# Paddle 简介

1. 2013年开始推出
2. 2016年开源
3. 2018正式开源

## paddle 安装指南

1. 使用pip安装paddle fluid的安装方式
2. docker容器封装编译

## paddle 架构

### 组网模块

- Python API

### 模型表达与优化

- 模型programs
- 统一中间表达
- 统一中间表达优化库

### 训练模块

- 训练RunTime
- CPU或者GPU集群

### 服务器预测

- 服务器预测API
- 服务器预测RunTime

### 移动端预测

- 移动端预测AIPI
- 移动端预测RunTime

## 组网模块基础概念

### layers

- layers输入和输出，是变量variable，变量可以是张量

### program

- 多个变量variable和layers组成program

### Executor

- Executor用来执行Programs。Executor会用一次性执行program中定义的所有的计算。可以通过feed来提供programs输入数据，通过fetch_list来获取输出数据

### feed/fetch_list

- Feed用来给模型的输入提供数据，fetch_list用来获取模型执行的中间结果

```python
from paddle import fluid
x = fluid.layers.fill_constant(shape=[1], dtype='int64', value=5)
y = fluid.layers.fill_constant(shape=[1], dtype='int64', value=1)
z = x + y

exe = fluid.Executor(fluid.CPUPlace())
exe.run(fluid.default_main_program(), fetch_list=[z])
```

## 模型进阶概念

### Control Flow

Paddle支持if-else和while等语法来描述灵活的模型逻辑，比如RNN会使用到while循环，learning rate scheduler可能使用到if-else判断。

```python
a = fluid.layers.fill_constant(shape=[2, 1], dtype='int64', value=5)
b = fluid.layers.fill_constant(shape=[2, 1], dtype='int64', value=6)
ifcond = fluid.layers.less_than(x=a, y=b)
ie = fluid.layers.ifElse(ifcond)
with ie.true.block():
    c = ie.input(a)
    c += 1
    ie.output(c)
# 因为a<b, c += 1被执行，所以c=6
exe.run(fluid.default_main_program(), fetch_list=[c])
```
