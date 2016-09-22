# -*- coding: utf-8 -*-
# 读入words,生成labelmap.prototxt格式文件
import os
import sys


'''
item {
  name: "none_of_the_above"
  label: 0
  display_name: "background"
}
'''
def writelabelmapfile(ftxt, string, count):
    ftxt.write('item {\n')
    ftxt.write('  name: "'+string+'"\n')
    ftxt.write('  label: '+str(count)+'\n')
    ftxt.write('  display_name: "'+string+'"\n')
    ftxt.write('}\n')

labelf = open('labelmap_voc.prototxt','w')
writelabelmapfile(labelf,'background',0)
word_fi = open("words.txt", 'r')
line_i = 0		
count=0
for line in word_fi.readlines():
    count=count+1
    writelabelmapfile(labelf,line.strip(),count)
word_fi.close()
labelf.close()
