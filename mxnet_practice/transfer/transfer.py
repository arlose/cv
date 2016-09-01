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
epoch_load = 10
sym, arg_params, aux_params = mx.model.load_checkpoint(model_prefix, epoch_load)

# init with pretrained weight
fixed_param_prefix = ['convolution0_bias', 'convolution1_bias', 'convolution2_bias','convolution0_weight', 'convolution1_weight', 'convolution2_weight']
for name in fixed_param_prefix:
    key = name
    if key in arg_params:
        arg_params[key].copyto(arg_dict[name])
    else:
        print("Skip argument %s" % name)

# new model
model_prefix="lenet_11"
begin_epoch=0
end_epoch=10

data_names = [k[0] for k in train_data.provide_data]
label_names = [k[0] for k in train_data.provide_label]
optimizer_params = {'momentum': 0.9,
                    'wd': 0.00001,
                    'learning_rate': 0.001,
                    'lr_scheduler': mx.lr_scheduler.FactorScheduler(1000, 0.9),
                    'rescale_grad': (1.0 / batch_size)}

# train set fixed_param_names
mod = mx.mod.Module(softmax, data_names=data_names, label_names=label_names,
                    logger=logger, context=ctx, work_load_list=None, fixed_param_names=fixed_param_prefix)

# load params to new model method 1 mod.init_params
mod.bind(data_shapes=train_data.provide_data, label_shapes=train_data.provide_label)
#mod.init_params(initializer=mx.init.Normal(0.02), arg_params=arg_dict, aux_params=aux_params, force_init=True)

# load params to new model method 2 mod.set_params
#mod.set_params(arg_params=arg_dict, aux_params=aux_params)

# load params to new model method 3 set arg_params=arg_dict, aux_params=aux_params in mod.fit
mod.fit(train_data, eval_data=val_data, eval_metric="accuracy", epoch_end_callback=mx.callback.do_checkpoint(model_prefix),
        batch_end_callback=mx.callback.Speedometer(batch_size, 50), 
        optimizer='sgd', optimizer_params=optimizer_params,
        arg_params=arg_dict, aux_params=aux_params, 
        begin_epoch=begin_epoch, num_epoch=end_epoch)

# below no fix param
'''
num_epoch = 10
model = mx.model.FeedForward(ctx=mx.gpu(), symbol=softmax, num_epoch=num_epoch,
                             learning_rate=0.001, momentum=0.9, wd=0.0001,
                             lr_scheduler=mx.lr_scheduler.FactorScheduler( step = 100 , factor = .9 ),
                             arg_params=arg_dict, aux_params=aux_params,)

model.fit(X=train_data,
          eval_data=val_data,
          eval_metric="accuracy",
          batch_end_callback=mx.callback.Speedometer(batch_size, 50),
          epoch_end_callback=mx.callback.do_checkpoint(model_prefix))
'''
