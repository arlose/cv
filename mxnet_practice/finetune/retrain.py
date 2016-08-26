import mxnet as mx
import logging
import lenet

logger = logging.getLogger()
logger.setLevel(logging.INFO)

batch_size = 32
data_shape = (1, 28, 28)

train = mx.io.ImageRecordIter(
        path_imgrec = "train2.rec",
        mean_img    = "mean.bin",
        data_shape  = data_shape,
        batch_size  = batch_size,
        rand_crop   = True,
        rand_mirror = True)

val = mx.io.ImageRecordIter(
        path_imgrec = "val1.rec",
        mean_img    = "mean.bin",
        data_shape  = data_shape,
        batch_size  = batch_size,
        rand_crop   = True,
        rand_mirror = True)

softmax = lenet.getsymbol()

num_epoch = 30
model_prefix = "lenet"
tmp_model = mx.model.FeedForward.load(model_prefix, num_epoch)

num_epoch = 10
model_prefix = "lenet_stage2"
model = mx.model.FeedForward(ctx=mx.gpu(), symbol=softmax, num_epoch=num_epoch,
                             learning_rate=0.001, momentum=0.9, wd=0.0001,
                             lr_scheduler=mx.lr_scheduler.FactorScheduler( step = 100 , factor = .9 ),
                             arg_params=tmp_model.arg_params, aux_params=tmp_model.aux_params,)

model.fit(X=train,
          eval_data=val,
          eval_metric="accuracy",
          batch_end_callback=mx.callback.Speedometer(batch_size, 50),
          epoch_end_callback=mx.callback.do_checkpoint(model_prefix))
