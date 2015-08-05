--convert the cnn weight and bias in the  'train.net' to txt file

require 'torch'
require 'nn'
require 'image'

--load the torch result file
net = torch.load('train.net')

--print(net)
print(#net.modules)
for i=1,#net.modules do
	print('-------------  ' .. i .. '  -------------')
	print(net.modules[i])
	print('input:')
	print(#net.modules[i].gradInput) 
	if net.modules[i].weight ~= nil then
		print('weight:')
		print(#net.modules[i].weight) 
		print('bias:')
		print(#net.modules[i].bias) 
	end
	print('output:')
	print(#net.modules[i].output) 
end

