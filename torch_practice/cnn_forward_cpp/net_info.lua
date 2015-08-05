--convert the cnn weight and bias in the  'train.net' to txt file

require 'torch'
require 'nn'
require 'image'

--load the torch result file
net = torch.load('train.net')

infofile=io.open('info.txt', 'w')
assert(infofile)

--print(net)

for i=1,#net.modules do
	infofile:write(i,' ')
	print('-------------  ' .. i .. '  -------------')
	print(net.modules[i])
	-- SpatialConvolution 	11
	-- ReLU 		12
	-- SpatialMaxPooling 	13
	-- Reshape		14
	-- Linear		15
	-- LogSoftMax		16
	str = tostring(net.modules[i])
	if string.find(str, 'SpatialConvolution') then
		infofile:write(11,' ')
	elseif string.find(str, 'ReLU') then
		infofile:write(12,' ')
	elseif string.find(str, 'MaxPooling') then
		infofile:write(13,' ')
	elseif string.find(str, 'Reshape') then
		infofile:write(14,' ')
	elseif string.find(str, 'Linear') then
		infofile:write(15,' ')
	elseif string.find(str, 'LogSoftMax') then
		infofile:write(16,' ')
	end
	print('input:')
	print(#net.modules[i].gradInput) 
	infofile:write(net.modules[i].gradInput:nDimension(),' ')
	for j=1,net.modules[i].gradInput:nDimension() do
		infofile:write(net.modules[i].gradInput:size()[j],' ')
	end
	if net.modules[i].weight ~= nil then
		print('weight:')
		print(#net.modules[i].weight) 
		infofile:write(net.modules[i].weight:nDimension(),' ')
		for j=1,net.modules[i].weight:nDimension() do
			infofile:write(net.modules[i].weight:size()[j],' ')
		end
		print('bias:')
		print(#net.modules[i].bias) 
		infofile:write(net.modules[i].bias:nDimension(),' ')
		for j=1,net.modules[i].bias:nDimension() do
			infofile:write(net.modules[i].bias:size()[j],' ')
		end
	else
		infofile:write(0,' ')
	end
	print('output:')
	print(#net.modules[i].output) 
	infofile:write(net.modules[i].output:nDimension(),' ')
	for j=1,net.modules[i].output:nDimension() do
		infofile:write(net.modules[i].output:size()[j],' ')
	end
	infofile:write('\n')
end

infofile:close()

