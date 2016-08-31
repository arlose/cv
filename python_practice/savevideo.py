import cv2
import os
import time
import numpy as np


cap = cv2.VideoCapture('test.mp4')
ret, im = cap.read()
print im.shape
filename = time.strftime("%m-%d-%H-%M-%S") + '.avi'

# opencv write only 5.7KB file 
# resolve: opencv 3.1.0
# sudo apt-get -y install libopencv-dev build-essential cmake git libgtk2.0-dev pkg-config python-dev python-numpy libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff4-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libxine-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libv4l-dev libtbb-dev libqt4-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils unzip
# cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D BUILD_opencv_gpu=OFF -D WITH_CUDA=OFF -D WITH_GSTREAMER_0_10=ON ..

#fourcc = cv2.cv.CV_FOURCC('m','p','4','v')
fourcc = cv2.VideoWriter_fourcc(*'XVID') # mp4v MJPG
out = cv2.VideoWriter(filename,fourcc, 20.0, (im.shape[1],im.shape[0]), True)
while(cap.isOpened()):
    ret, im = cap.read()
    if ret is False:
        break
    out.write(im)
    #cv2.imshow("show", im)
    #cv2.waitKey(1)
cap.release()
out.release()
'''

# skvideo 
# sudo apt-get install libav-tools
# sudo pip install scikit-video

from skvideo.io import VideoWriter
writer = VideoWriter(filename, frameSize=(im.shape[1], im.shape[0]))
writer.open()
while(cap.isOpened()):
    ret, im = cap.read()
    if ret is False:
        break
    writer.write(im)
    cv2.imshow("show", im)
    cv2.waitKey(1)
writer.release()
'''
