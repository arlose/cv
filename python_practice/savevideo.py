import cv2
import os
import time
import numpy as np

cap = cv2.VideoCapture('test.mp4')
ret, im = cap.read()

print im.shape

filename = time.strftime("%m-%d-%H-%M-%S") + '.avi'
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
#fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
out = cv2.VideoWriter(filename,fourcc, 20.0, (im.shape[0],im.shape[1]), True)
i=0
while(cap.isOpened()):
    ret, im = cap.read()
    out.write(im)
    cv2.imshow("show", im)
    cv2.waitKey(1)
    print i
    i=i+1
cap.release()
out.release()
