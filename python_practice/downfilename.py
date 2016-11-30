# -*- coding: utf-8 -*-
"""
@author: fengjie
随机选取VOC中的一部分,便于训练小数据并验证
"""
import os
import random

# 抽取比率
extractratio = 0.2

filename = './VOC2007/ImageSets/Main/trainval.txt'
newfilename = './VOC2007/ImageSets/Main/all.txt'
otherfilename = './VOC2007/ImageSets/Main/other.txt'

lines = []
# 读取ImageSets/Main/trainval.txt
fin = open(filename, 'r')
for line in fin.readlines():
    lines.append(line)
fin.close()

random.shuffle(lines)

# 文件重命名
os.rename(filename, newfilename)

# 随机选取部分存入新的trainval.txt中
number = len(lines)
newnumber = int(number*extractratio)
fout = open(filename, 'w')
for i in range(newnumber):
    fout.write(lines[i])
fout.close()
# 剩余的部分存入other.txt
fout = open(otherfilename, 'w')
for i in range(newnumber, number):
    fout.write(lines[i])
fout.close()




