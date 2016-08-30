# coding: utf-8

import cv2
import numpy as np

# 图像大小
width = 200
height = 100

# 各个端点，以小数形式表示
p=[(0.1,0.2),(0.2,0.1),(0.8,0.3),(0.7,0.9),(0.3,0.8),(0.2,0.4)]
pointnum = 6

# 生成一个黑色图像
img = np.zeros((height, width))

# 画多边形填充区域
pts=[]
for i in range(0, pointnum):
    point = [int(p[i][0]*width+0.5), int(p[i][1]*height+0.5)]
    pts.append(point)
pts1 = np.array(pts, np.int32)
cv2.fillConvexPoly(img, pts1, 1)

# 显示
cv2.namedWindow('image')
cv2.imshow('image', img)
cv2.waitKey(0)


