import mxnet as mx

def getsymbol(num):
	data = mx.symbol.Variable('data')
	# first conv
	conv1 = mx.symbol.Convolution(data=data, kernel=(3,3), num_filter=8)
	relu1 = mx.symbol.Activation(data=conv1, act_type="relu")
	pool1 = mx.symbol.Pooling(data=relu1, pool_type="max",
		                  kernel=(2,2), stride=(2,2))
	# second conv
	conv2 = mx.symbol.Convolution(data=pool1, kernel=(3,3), num_filter=16)
	relu2 = mx.symbol.Activation(data=conv2, act_type="relu")
	pool2 = mx.symbol.Pooling(data=relu2, pool_type="max",
		                  kernel=(2,2), stride=(2,2))
        # third conv
	conv3 = mx.symbol.Convolution(data=pool2, kernel=(3,3), num_filter=16)
	relu3 = mx.symbol.Activation(data=conv3, act_type="relu")
	pool3 = mx.symbol.Pooling(data=relu3, pool_type="max",
		                  kernel=(2,2), stride=(2,2))
	# first fullc
	flatten = mx.symbol.Flatten(data=pool3)
	fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=num)
	# loss
	lenet = mx.symbol.SoftmaxOutput(data=fc1, name='softmax')
	
	return lenet
