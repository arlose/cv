# -*- coding: utf-8 -*-
# 判断jpg文件能否采用cv2来打开
import os
import cv2
import string

suffix_list=['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']
count = 0
for fpathe,dirs,fs in os.walk('./VOC2007'):
  for f in fs:
    if os.path.splitext(f)[1] in suffix_list:
      imagefile = os.path.join(fpathe,f)
      print imagefile
      img = cv2.imread(imagefile,1)
      print img.shape
      count = count + 1
print count
