import argparse
import logging
import os
import sys

import cv2
import mxnet as mx
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score

from lightened_cnn import lightened_cnn_b_feature
# load model
ctx = mx.gpu(0)
_, model_args, model_auxs = mx.model.load_checkpoint('./lightened_cnn/lightened_cnn', 166)
symbol = lightened_cnn_b_feature()

# load data0
size=128
img_arr=np.zeros((1,1,size,size),dtype=float)
img=np.expand_dims(cv2.imread("test.png",0),axis=0)
img_arr[0][:]=img/255.0

# caculate feature0
model_args['data']=mx.nd.array(img_arr, ctx)
exector = symbol.bind(ctx, model_args ,args_grad=None, grad_req="null", aux_states=model_auxs)
exector.forward(is_train=False)
output0 = exector.outputs[0].asnumpy()

# load data1
img=np.expand_dims(cv2.imread("test1.png",0),axis=0)
img_arr[0][:]=img/255.0
# caculate feature1
model_args['data']=mx.nd.array(img_arr, ctx)
exector = symbol.bind(ctx, model_args ,args_grad=None, grad_req="null", aux_states=model_auxs)
exector.forward(is_train=False)
output1 = exector.outputs[0].asnumpy()

# calculate the similarity
dotacc=np.dot(output0[0],output1[0])/np.linalg.norm(output0[0])/np.linalg.norm(output1[0])

print dotacc

th = 0.305
if(dotacc>th):
    print 'same'
else:
    print 'not same'

