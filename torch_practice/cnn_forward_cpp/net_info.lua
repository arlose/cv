--convert the cnn weight and bias in the  'train.net' to txt file

require 'torch'
require 'nn'
require 'image'

--load the torch result file
net = torch.load('train.net')

--save the net infomation to txt
infofile=io.open('info.txt', 'w')
assert(infofile)

--save the net to txt
file=io.open('train.txt', 'w')
assert(file)

--print(net)
infofile:write(#net.modules,'\n')

for i=1,#net.modules do
	print('-------------  ' .. i .. '  -------------')
	print(net.modules[i])
	-- SpatialConvolution 	11
	-- TanH 		12
	-- ReLU 		13
	-- SpatialMaxPooling 	14
	-- Reshape		15
	-- Linear		16
	-- LogSoftMax		17
	str = tostring(net.modules[i])
	if string.find(str, 'SpatialConvolution') then
		infofile:write(11,' ')
	elseif string.find(str, 'TanH') then
		infofile:write(12,' ')
	elseif string.find(str, 'ReLU') then
		infofile:write(13,' ')
	elseif string.find(str, 'MaxPooling') then
		infofile:write(14,' ')
	elseif string.find(str, 'Reshape') then
		infofile:write(15,' ')
	elseif string.find(str, 'Linear') then
		infofile:write(16,' ')
	elseif string.find(str, 'LogSoftMax') then
		infofile:write(17,' ')
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
		wd = net.modules[i].weight:nDimension()
		infofile:write(wd,' ')
		for j=1,net.modules[i].weight:nDimension() do
			infofile:write(net.modules[i].weight:size()[j],' ')
		end
		-- weight dimension max 4
		assert(wd<5)
		if wd == 4 then
			ws1 = net.modules[i].weight:size()[1]
			ws2 = net.modules[i].weight:size()[2]
			ws3 = net.modules[i].weight:size()[3]
			ws4 = net.modules[i].weight:size()[4]
			for k=1,ws1 do
				for l=1,ws2 do
					for m=1,ws3 do
						for n=1,ws4 do
							file:write(net.modules[i].weight[k][l][m][n],' ')
						end
					end
				end
			end
			file:write('\n')
		elseif wd == 3 then
			ws1 = net.modules[i].weight:size()[1]
			ws2 = net.modules[i].weight:size()[2]
			ws3 = net.modules[i].weight:size()[3]
			for l=1,ws1 do
				for m=1,ws2 do
					for n=1,ws3 do
						file:write(net.modules[i].weight[l][m][n],' ')
					end
				end
			end
			file:write('\n')
		elseif wd == 2 then
			ws1 = net.modules[i].weight:size()[1]
			ws2 = net.modules[i].weight:size()[2]
			for m=1,ws1 do
				for n=1,ws2 do
					file:write(net.modules[i].weight[m][n],' ')
				end
			end
			file:write('\n')
		elseif wd == 1 then
			ws1 = net.modules[i].weight:size()[1]
			for n=1,ws1 do
				file:write(net.modules[i].weight[n],' ')
			end
			file:write('\n')
		end
		
		print('bias:')
		print(#net.modules[i].bias) 
		bd = net.modules[i].bias:nDimension()
		infofile:write(bd,' ')
		-- bias always has dimension of 1
		assert(bd==1)
		for j=1,net.modules[i].bias:nDimension() do
			infofile:write(net.modules[i].bias:size()[j],' ')
		end
		bs = net.modules[i].bias:size()[1]
		for n=1,bs do
			file:write(net.modules[i].bias[n],' ')
		end
		file:write('\n')
		
	else
		infofile:write(0,' ') --weight
		infofile:write(0,' ') --bias
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
file:close()

