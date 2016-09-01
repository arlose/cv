# coding: utf-8
'''
transfer learning network
11 classes
'''
import mxnet as mx
import logging
import lenet

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ctx=mx.gpu(0)

batch_size = 32
data_shape = (3, 28, 28)

train_data = mx.io.ImageRecordIter(
        path_imgrec = "train2_11.rec",
        mean_img    = "mean.bin",
        data_shape  = data_shape,
        batch_size  = batch_size,
        rand_crop   = True,
        rand_mirror = True)

val_data = mx.io.ImageRecordIter(
        path_imgrec = "val2_11.rec",
        mean_img    = "mean.bin",
        data_shape  = data_shape,
        batch_size  = batch_size,
        rand_crop   = True,
        rand_mirror = True)

number = 11
softmax = lenet.getsymbol(number)

arg_shapes, output_shapes, aux_shapes = softmax.infer_shape(data=(1, 3, data_shape[1], data_shape[2]))
arg_names = softmax.list_arguments()
arg_dict = dict(zip(arg_names, [mx.nd.zeros(shape, ctx=ctx) for shape in arg_shapes]))

# load pretrained
model_prefix = "lenet_10"
num_epoch = 10
pretrainedname = model_prefix + ("-%04d"%num_epoch) + ".params"
pretrained = mx.nd.load(pretrainedname)

# init with pretrained weight
fixed_param_prefix = ['convolution0_bias', 'convolution1_bias', 'convolution2_bias','convolution0_weight', 'convolution1_weight', 'convolution2_weight']
for name in fixed_param_prefix:
    key = "arg:" + name
    if key in pretrained:
        pretrained[key].copyto(arg_dict[name])
    else:
        print("Skip argument %s" % name)

# new model
model_prefix="lenet_11"
begin_epoch=0
end_epoch=10
fixed_param_prefix = ['convolution0', 'convolution1', 'convolution2']
data_names = [k[0] for k in train_data.provide_data]
label_names = [k[0] for k in train_data.provide_label]
optimizer_params = {'momentum': 0.9,
                    'wd': 0.00001,
                    'learning_rate': 0.001,
                    'lr_scheduler': mx.lr_scheduler.FactorScheduler(1000, 0.1),
                    'rescale_grad': (1.0 / batch_size)}

# train
mod = mx.mod.Module(softmax, data_names=data_names, label_names=label_names,
                    logger=logger, context=ctx, work_load_list=None,
                    fixed_param_names=fixed_param_prefix)
mod.bind(data_shapes=train_data.provide_data,
         label_shapes=train_data.provide_label)
mod.init_params(initializer=mx.init.Normal(0.02), arg_params=arg_dict, force_init=True)

mod.fit(train_data, eval_data=val_data, eval_metric="accuracy", epoch_end_callback=mx.callback.do_checkpoint(model_prefix),
        batch_end_callback=mx.callback.Speedometer(batch_size, 50), 
        optimizer='sgd', optimizer_params=optimizer_params,
        #arg_params=args, aux_params=auxs, 
        begin_epoch=begin_epoch, num_epoch=end_epoch)

