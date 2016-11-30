# -*- coding: utf-8 -*-
"""
@author: fengjie
生成trainval.txt和test.txt
"""
import os
import uniout 
import sys
import string
import random

suffix_list=['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']

# 测试比率
testratio = 0.2

trainvalname = './VOC2007/ImageSets/Main/trainval.txt'
testname = './VOC2007/ImageSets/Main/test.txt'

VOC2007Path = './VOC2007'
AnnotationsPath = VOC2007Path+'/Annotations'
JPEGImagesPath = VOC2007Path+'/JPEGImages'

lines = []

# 读取JPEGImages文件夹下的图片和Annotations下的标注，如果两者都存在，则放到lines中
count = 0
for fpathe,dirs,fs in os.walk(JPEGImagesPath):
  for f in fs:
    if os.path.splitext(f)[1] in suffix_list:
      imagefile = os.path.join(fpathe,f)
      labelfile = os.path.join(fpathe,f).replace('jpg','xml')
      labelfile = labelfile.replace('JPEGImages','Annotations')
      filename = os.path.basename(imagefile).split('.')[-2]
      if os.path.exists(labelfile):
        lines.append(filename)
        count = count + 1
print 'total image number:' + str(count)

random.shuffle(lines)
number = len(lines)
testnumber = int(number*testratio)

ftxt = open(trainvalname,'w')
for i in range(number-testnumber):
  ftxt.write(lines[i]+'\n')
ftxt.close()

ftxt = open(testname,'w')
for i in range(number-testnumber, number):
  ftxt.write(lines[i]+'\n')
ftxt.close()


