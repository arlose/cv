# coding: utf-8
'''
base network module
10 classes
'''
import mxnet as mx
import logging
import lenet

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

batch_size = 32
data_shape = (3, 28, 28)
train = mx.io.ImageRecordIter(
        path_imgrec = "train1_10.rec",
        mean_img    = "mean.bin",
        data_shape  = data_shape,
        batch_size  = batch_size,
        rand_crop   = True,
        rand_mirror = True)
val = mx.io.ImageRecordIter(
        path_imgrec = "val1_10.rec",
        mean_img    = "mean.bin",
        data_shape  = data_shape,
        batch_size  = batch_size,
        rand_crop   = True,
        rand_mirror = True)

number = 10
softmax = lenet.getsymbol(number)

num_round = 30
num_gpu = 1
gpus = [mx.gpu(i) for i in range(num_gpu)]

model = mx.model.FeedForward(ctx=gpus, symbol=softmax, num_epoch=num_round,
                             learning_rate=0.001, momentum=0.9, wd=0.00001)
model_prefix = "lenet_10"
model.fit(X=train, eval_data=val,
          eval_metric="accuracy",
          batch_end_callback=mx.callback.Speedometer(batch_size, 50),
          epoch_end_callback=mx.callback.do_checkpoint(model_prefix))
