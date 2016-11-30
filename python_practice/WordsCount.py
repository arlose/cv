# -*- coding: utf-8 -*-
import os
import sys
import string
# 解决中文打印问题 sudo pip install uniout
import uniout

filecount = 0
suffix_list=['.txt']
# txt文件夹
txtpath = './Annotations'

# 读入words，初始化类别
listwords=[]
word_fi = open("words.txt", 'r')
for line in word_fi.readlines():
  listwords.append(line.strip())
word_fi.close()
dictwords = dict.fromkeys(listwords,0)

# 读入txt文件，统计计数
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

def countword(dictwords, rects):
  if rects is None:
    return
  else:
    try:
      for rect in rects:
        dictwords[rect[4]] = dictwords[rect[4]] + 1
    except:
      print rects


for fpathe,dirs,fs in os.walk(txtpath):
  for f in fs:
    if os.path.splitext(f)[1] in suffix_list:
      labelfile = os.path.join(fpathe,f)
      rects = readrects(labelfile)
      countword(dictwords,rects)
      filecount=filecount+1
print filecount
print dictwords

