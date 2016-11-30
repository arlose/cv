# -*- coding: utf-8 -*-
import os
import cv2
import string
import xml.dom

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

def create_element(doc,tag,attr):
  #创建一个元素节点
  elementNode=doc.createElement(tag)
  #创建一个文本节点
  textNode=doc.createTextNode(attr)
  #将文本节点作为元素节点的子节点
  elementNode.appendChild(textNode)
  return elementNode

def genxml(filename, width, height, rects):
  dom1=xml.dom.getDOMImplementation()#创建文档对象，文档对象用于创建各种节点。
  doc=dom1.createDocument(None,"annotation",None)
  top_element = doc.documentElement# 得到根节点

  #folder and filename
  folderNode=create_element(doc,'folder','MIDDLE')
  filenameNode=create_element(doc,'filename',filename+'.jpg')
  top_element.appendChild(folderNode)
  top_element.appendChild(filenameNode)

  #source
  sourceNode=doc.createElement('source')
  databaseNode=create_element(doc,'database','Middle Database')
  annoNode=create_element(doc,'annotation','Middle')
  imageNode=create_element(doc,'image','flickr')
  sourceNode.appendChild(databaseNode)
  sourceNode.appendChild(annoNode)
  sourceNode.appendChild(imageNode)
  top_element.appendChild(sourceNode)

  #size
  sizeNode=doc.createElement('size')
  widthNode=create_element(doc,'width',str(width))
  heightNode=create_element(doc,'height',str(height))
  depthNode=create_element(doc,'depth','3')
  sizeNode.appendChild(widthNode)
  sizeNode.appendChild(heightNode)
  sizeNode.appendChild(depthNode)
  top_element.appendChild(sizeNode)

  #segmented
  segmentedNode=create_element(doc,'segmented','0')
  top_element.appendChild(segmentedNode)
  
  if rects is None:
    return
  else:
    for rect in rects:
      #object
      objNode=doc.createElement('object')
      nameNode=create_element(doc,'name',rect[4])
      poseNode=create_element(doc,'pose','Unspecified')
      truncatedNode=create_element(doc,'truncated','0')
      difficultNode=create_element(doc,'difficult','0')
      bndboxNode=doc.createElement('bndbox')
      xmin = max(int(rect[0]), 1)
      ymin = max(int(rect[1]), 1)
      xmax = min(int(rect[2]), width-1)
      ymax = min(int(rect[3]), height-1)
      if xmin > xmax:
        xmax = xmin+1
      if ymin > ymax:
        ymax = ymin+1
      xminNode=create_element(doc,'xmin',str(xmin))
      yminNode=create_element(doc,'ymin',str(ymin))
      xmaxNode=create_element(doc,'xmax',str(xmax))
      ymaxNode=create_element(doc,'ymax',str(ymax))
      bndboxNode.appendChild(xminNode)
      bndboxNode.appendChild(yminNode)
      bndboxNode.appendChild(xmaxNode)
      bndboxNode.appendChild(ymaxNode)
      objNode.appendChild(nameNode)
      objNode.appendChild(poseNode)
      objNode.appendChild(truncatedNode)
      objNode.appendChild(difficultNode)
      objNode.appendChild(bndboxNode)
      top_element.appendChild(objNode)

  xmlfile=open('./VOC2007/Annotations/'+filename+'.xml','w')
  doc.writexml(xmlfile,addindent=' '*4, newl='\n', encoding='utf-8')
  xmlfile.close()

for fpathe,dirs,fs in os.walk('./VOC2007'):
  for f in fs:
    if os.path.splitext(f)[1] in suffix_list:
      imagefile = os.path.join(fpathe,f)
      labelfile = os.path.join(fpathe,f).replace('jpg','txt')
      labelfile = labelfile.replace('JPEGImages','Annotations')
      xmlfile = labelfile.replace('txt','xml')
      if(not os.path.exists(xmlfile)):
        img = cv2.imread(imagefile,1)
        rects = readrects(labelfile)
        filename = os.path.basename(imagefile).split('.')[-2]
        print filename
        (width,height,_) = img.shape
        if len(rects) > 0:
          genxml(filename, width, height, rects)
          count = count + 1
print count
