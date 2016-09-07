# -*- coding: utf-8 -*-
# 移除没有标记的文件，重新生成trainval.txt
import os
import cv2
import string
import shutil

suffix_list=['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']
count = 0

def readrects(labelfile):
  try:
    file_object = open(labelfile, 'r')
    list_of_all_the_lines = file_object.readlines( )
    num = string.atoi(list_of_all_the_lines[0])
    rects = []
    for i in range(1,num+1) :
      rect = list_of_all_the_lines[i].split()
      rects.append(rect)
    file_object.close()
    return rects
  except IOError:
    return None

VOC2007Path = './VOC2007'
AnnotationsPath = VOC2007Path+'/Annotations'
ImageSetsPath = VOC2007Path+'/ImageSets'
JPEGImagesPath = VOC2007Path+'/JPEGImages'

ftxt = open(ImageSetsPath+'/Main/trainval.txt','w')
for fpathe,dirs,fs in os.walk(VOC2007Path):
  for f in fs:
    if os.path.splitext(f)[1] in suffix_list:
      imagefile = os.path.join(fpathe,f)
      labelfile = os.path.join(fpathe,f).replace('jpg','txt')
      labelfile = labelfile.replace('JPEGImages','Annotations')
      rects = readrects(labelfile)
      filename = os.path.basename(imagefile).split('.')[-2]
      if len(rects)==0:
        print filename
        shutil.move(imagefile, VOC2007Path+'/unused/')
        shutil.move(labelfile, VOC2007Path+'/unused/')
      else:
        ftxt.write(filename+'\n')
        count = count + 1
print count
ftxt.close()
