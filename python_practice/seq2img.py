import argparse
import os
import numpy as np
import cv2
import os.path

def seq2img(videopath, skipnum, rszratio):
    capture=cv2.VideoCapture(videopath)
    videoname = os.path.basename(videopath).split('.')[-2]
    if not os.path.exists(videoname):
        os.makedirs(videoname)
    n=1
    ret, im = capture.read()
    img = cv2.resize(im,None,fx=rszratio, fy=rszratio, interpolation = cv2.INTER_CUBIC)
    imgname = videoname+'/'+str(n)+'.jpg'
    cv2.imwrite(imgname, img)
    

    while True:
        for i in range(0,skipnum):
            ret, im = capture.read()
            n = n+1
        ret, im = capture.read()
        img = cv2.resize(im,None,fx=rszratio, fy=rszratio, interpolation = cv2.INTER_CUBIC)
        imgname = videoname+'/'+str(n)+'.jpg'
        cv2.imwrite(imgname, img)
        print n

def parse_args():
    parser = argparse.ArgumentParser(description='Segment a video to images')
    parser.add_argument('--video', dest='video', help='custom video', default='test.ts', type=str)
    parser.add_argument('--skip', dest='skip', help='skip number', default=30, type=int)
    parser.add_argument('--ratio', dest='ratio', help='resize ratio', default=0.5, type=float)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    seq2img(args.video, args.skip, args.ratio)
