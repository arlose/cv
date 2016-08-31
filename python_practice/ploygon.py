# coding: utf-8

import cv2
import numpy as np

# 图像大小
width = 200
height = 100

# 各个端点，以小数形式表示
p=[(0.0,0.0),(0.2,0.1),(0.8,0.3),(0.7,0.9),(0.3,0.8),(0.2,0.4)]
pointnum = len(p)

# 生成一个黑色图像
img = np.zeros((height, width))#, dtype=np.uint8)

# 画多边形填充区域
pts=[]
for i in range(0, pointnum):
    point = [int(p[i][0]*width+0.5), int(p[i][1]*height+0.5)]
    pts.append(point)
pts1 = np.array(pts, np.int32)
cv2.fillConvexPoly(img, pts1, 1)

# 形态滤波，反色，色彩转换
img1 = np.uint8(img*255)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7, 7)) 
res = cv2.dilate(img1,kernel)
#res = cv2.erode(img1,kernel)
#res = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel) 
#res = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)  
ret, res = cv2.threshold(res,127,255,cv2.THRESH_BINARY_INV) 
result = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB)

# 显示
cv2.namedWindow('image')
cv2.imshow('image', img)
cv2.namedWindow('res')
cv2.imshow('res', result)
cv2.waitKey(0)


