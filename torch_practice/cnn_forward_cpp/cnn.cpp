#include "cnn.h"
#include <fstream>
#include <iostream>
#include <iomanip>

using namespace std;

cnn::cnn()
{

}

cnn::~cnn()
{

}

double relu(double x)
{
	if(x>0.0)
		return x;
	else
		return 0.0;
}

double softmax(double x)
{
	return (1/(1+exp(-1*x)));
}



bool cnn::getImg(Mat matImg)
{
	
	if(matImg.empty())
	{
		return false;
	}
	else
	{
	    	int ch = matImg.channels();
		int width = matImg.cols;
		int height = matImg.rows;
		
		input = new double[ch*width*height];

	    	if(ch==3)
		{
		    	for(int t=0; t<ch; t++)
		    	{
		        	for (int row = 0; row < height; row++)
		        	{
					for (int col = 0; col < width; col++)
					{
						input[t*width*height+row*width+col] = ((static_cast<double>(*(matImg.data + matImg.step[0] * row + matImg.step[1] * col + matImg.elemSize1() * (2-t))) / 255)-0.5)*2;
					}
				}
			}
		}	
		else if(ch==1)
		{
			for (int row = 0; row < height; row++)
	        	{
				for (int col = 0; col < width; col++)
				{
					input[row*width+col] = ((static_cast<double>(*(matImg.data + matImg.step[0] * row + matImg.step[1] * col)) / 255)-0.5)*2;
				}
			}
		}	
		return true;
	}
}

bool cnn::loadModelInfo(string filename)
{
	ifstream infile(filename.c_str());
	if(!infile.is_open())
	{
		return false;
	}
	// init
	memset(&info, 0, sizeof(SLayerInfo));
	for(int i=0;i<MAXLAYERNUM;i++)
		for(int j=0;j<MAXDIMSIZE;j++)
		{
			info.weightsize[i][j] = 1;
			info.biassize[i][j] = 1;
		}
	// read the info
	infile>>info.layernumber;
	for(int i=0;i<info.layernumber;i++)
	{
		int j;
		infile>>info.type[i];
		infile>>info.inputdim[i];
		for(j=0;j<info.inputdim[i];j++)
			infile>>info.inputsize[i][j];
		infile>>info.weightdim[i];
		for(j=0;j<info.weightdim[i];j++)
			infile>>info.weightsize[i][j];
		infile>>info.biasdim[i];
		for(j=0;j<info.biasdim[i];j++)
			infile>>info.biassize[i][j];
		infile>>info.outputdim[i];
		for(j=0;j<info.outputdim[i];j++)
			infile>>info.outputsize[i][j];
	}
	return true;
	
}

bool cnn::loadModel(string filename)
{
	ifstream infile(filename.c_str());
	if(!infile.is_open())
	{
		return false;
	}

	for(int i=0;i<info.layernumber;i++)
	{
		int weightsize = 1;
		int biassize = 1;
		if(info.weightdim[i]>0)
		{
			for(int j=0;j<info.weightdim[i];j++)
			{
				weightsize *= info.weightsize[i][j];
			}
			layer_weight[i] = new double[weightsize];
			for(int j=0;j<weightsize;j++)
{
				infile>>layer_weight[i][j];
}
		}
		if(info.biasdim[i]>0)
		{
			for(int j=0;j<info.biasdim[i];j++)
			{
				biassize *= info.biassize[i][j];
			}
			layer_bias[i] = new double[biassize];
			for(int j=0;j<biassize;j++)
				infile>>layer_bias[i][j];
		}
		
	}

	return true;
}

Soutput cnn::forward()
{
        Soutput o;
	
	double *lin = NULL;

	for(int l=0;l<info.layernumber;l++)
	{
		int outputsize = 1;
		for(int j=0;j<info.outputdim[l];j++)
		{
			outputsize *= info.outputsize[l][j];
		}
		layer_output[l] = new double[outputsize];

		if(l!=0)
			lin = layer_output[l-1];
		else
			lin = input;
		int smpw, smph, wxh, ismpw, ismph, iwxh;
		
		switch(info.type[l])
		{
			case 11: // SpatialConvolution
				printf("layer %d SpatialConvolution\n", l+1);
				int d1,d2,d3,d4,w,h,iw,ih;
				if(info.weightdim[l]==4)
				{
					d1 = info.weightsize[l][0];
					d2 = info.weightsize[l][1];
					d3 = info.weightsize[l][2];
					d4 = info.weightsize[l][3];
				}
				if(info.weightdim[l]==3)
				{
					d1 = info.weightsize[l][0];
					d2 = 1;
					d3 = info.weightsize[l][1];
					d4 = info.weightsize[l][2];
				}
				if(info.outputdim[l]==2)
				{
					h = info.outputsize[l][0];
					w = info.outputsize[l][1];
				}
				if(info.outputdim[l]==3)
				{
					h = info.outputsize[l][1];
					w = info.outputsize[l][2];
				}
				if(info.inputdim[l]==2)
				{
					ih = info.inputsize[l][0];
					iw = info.inputsize[l][1];
				}
				if(info.inputdim[l]==3)
				{
					ih = info.inputsize[l][1];
					iw = info.inputsize[l][2];
				}
				
				for(int t=0; t<d1; ++t)//layer to
				{
					for(int i=0; i<h; ++i)//to image row
					{
						for(int j=0; j<w; ++j)//to image col
						{
							layer_output[l][t*h*w+i*w+j] = 0;
							for(int f=0; f<d2; ++f)//layer from
							{
								for(int m=0; m<d3; ++m)//filter row
								{
									for(int n=0; n<d4; ++n)//filter col
									{
										layer_output[l][t*h*w+i*w+j] += lin[f*iw*ih+(i+m)*iw+j+n] * layer_weight[l][t*d2*d3*d4+f*d3*d4+m*d4+n];
									}
								}
							}

						        layer_output[l][t*h*w+i*w+j] += layer_bias[l][t];
						        
						}
					}
				}
				
				break ;
			case 12: // TanH
				printf("layer %d TanH\n", l+1);
				for(int i=0;i<outputsize;i++)
					layer_output[l][i] = tanh(lin[i]);
				break ;
			case 13: // ReLU
				printf("layer %d ReLU\n", l+1);
				for(int i=0;i<outputsize;i++)
					layer_output[l][i] = relu(lin[i]);
				break ;
			case 14: // SpatialMaxPooling
				printf("layer %d SpatialMaxPooling\n", l+1);
				double maxm[2];
				
				smpw = info.outputsize[l][2];
				smph = info.outputsize[l][1];
				wxh = info.outputsize[l][2]*info.outputsize[l][1];
				ismpw = info.inputsize[l][2];
				ismph = info.inputsize[l][1];
				iwxh = info.inputsize[l][2]*info.inputsize[l][1];
				for(int t=0; t<info.outputsize[l][0]; ++t)
				{
					for(int i=0; i<smph; ++i)
					{
						for(int j=0; j<smpw; ++j)
						{
						        maxm[0] = max(lin[t*iwxh+2*i*ismpw+2*j],lin[t*iwxh+2*i*ismpw+2*j+1]);
						        maxm[1] = max(lin[t*iwxh+(2*i+1)*ismpw+2*j],lin[t*iwxh+(2*i+1)*ismpw+2*j+1]);
						        layer_output[l][t*wxh+i*smpw+j] = max(maxm[0],maxm[1]);
						}
					}
				}


				break ;
			case 15: // Reshape
				printf("layer %d Reshape\n", l+1);
				int idx;
				int rh,rw,rd;
				if(info.inputdim[l]==2)
				{
					rd = 1;
					rh = info.inputsize[l][0];
					rw = info.inputsize[l][1];
				}
				if(info.inputdim[l]==3)
				{
					rd = info.inputsize[l][0];
					rh = info.inputsize[l][1];
					rw = info.inputsize[l][2];
				}
				idx = 0;
				for(int t=0; t<rd; ++t)
				{
					for(int i=0; i<rh; ++i)
					{
						for(int j=0; j<rw; ++j)
						{
						        layer_output[l][idx++] = lin[t*rw*rh+i*rw+j];
						}
					}
				}
				break ;
			case 16: // Linear
				printf("layer %d Linear\n", l+1);
				for(int t=0; t<outputsize; ++t)
				{
					layer_output[l][t] = 0;
					for(int f=0; f<info.inputsize[l][0]; ++f)
					{
						layer_output[l][t] += lin[f] * layer_weight[l][t*info.inputsize[l][0]+f];
					}
					layer_output[l][t] += layer_bias[l][t];
				}
				break ;
			case 17: // LogSoftMax DO NOTHING
				printf("layer %d LogSoftMax\n", l+1);
				for(int i=0;i<outputsize;i++)
					layer_output[l][i] = lin[i];
				break ;
			default:
				cout<<"unknow type: "<<l<<" "<<info.type[l]<<endl;
				break ;
		}
		if(l==100)
		{
			for(int i=0;i<29;i++)
				printf("%lf\n", layer_output[l][i]);
		}
	}

        double maxVal = layer_output[info.layernumber-1][0];
	int maxIdx = 0;
	o.score = new double[info.outputsize[info.layernumber-1][0]];
        for(int i=0; i<info.outputsize[info.layernumber-1][0]; ++i)
	{
                if(layer_output[info.layernumber-1][i] > maxVal)
		{
                        maxVal = layer_output[info.layernumber-1][i];
			maxIdx = i;
		}
                o.score[i]=layer_output[info.layernumber-1][i];
	}

        o.idx = maxIdx + 1; //because the index of the label data is from 1
	
        return o;
}

#if 0

/*
model:add(nn.SpatialConvolution(3, 8, 3, 3))
model:add(nn.ReLU())
*/
//conv1 and relu2 3*64*64 ------ 8*62*62
void cnn::forward12()
{
	for(int t=0; t<8; ++t)//layer to
	{
                for(int i=0; i<62; ++i)//to image row
		{
                        for(int j=0; j<62; ++j)//to image col
			{
				conv1relu2[t][i][j] = 0;
				for(int f=0; f<3; ++f)//layer from
				{
					for(int m=0; m<3; ++m)//filter row
					{
						for(int n=0; n<3; ++n)//filter col
						{
							conv1relu2[t][i][j] += img[f][i+m][j+n] * conv1Weight[t][f][m][n];
						}
					}
				}

                                conv1relu2[t][i][j] += conv1Bias[t];
                                conv1relu2[t][i][j] = relu(conv1relu2[t][i][j]);
                               // if(t==0&&i==0)
                                   // printf("%lf\n", conv1relu2[t][i][j]);
			}
		}
	}
}

/*
model:add(nn.SpatialLPPooling(16,2, 2, 2, 2, 2))
*/
//pooling3 8*62*62 ------- 8*31*31
void cnn::forward3()
{
        double maxm[2];
        for(int t=0; t<8; ++t)
	{
                for(int i=0; i<31; ++i)
		{
                        for(int j=0; j<31; ++j)
			{
                                maxm[0] = max(conv1relu2[t][2*i][2*j],conv1relu2[t][2*i][2*j+1]);
                                maxm[1] = max(conv1relu2[t][2*i+1][2*j],conv1relu2[t][2*i+1][2*j+1]);
                                pooling3[t][i][j] = max(maxm[0],maxm[1]);
                                //printf("%lf   ", pooling3[t][i][j]);
			}
                        //printf("\n");
                }
                //printf("\n");
	}
}

/*
--model:add(nn.SpatialConvolution(8, 16, 3, 3, 1, 1, 1))
--model:add(nn.ReLU())
*/
//conv4 and relu5 16*31*31 -------- 16*29*29
void cnn::forward45()
{
        for(int t=0; t<16; ++t)
	{
                for(int i=0; i<29; ++i)
		{
                        for(int j=0; j<29; ++j)
			{
                                conv4relu5[t][i][j] = 0;
                                for(int f=0; f<8; ++f)
				{
                                        for(int m=0; m<3; ++m)
					{
                                                for(int n=0; n<3; ++n)
						{
                                                        conv4relu5[t][i][j] += pooling3[f][i+m][j+n] * conv4Weight[t][f][m][n];
						}
					}
				}
                                conv4relu5[t][i][j] += conv4Bias[t];

                                conv4relu5[t][i][j] = relu(conv4relu5[t][i][j]);
                                //if(t==5&&i==0)
                                      // printf("%lf\n", conv4relu5[t][i][j]);

			}
		}
	}
}
/*
--model:add(nn.SpatialMaxPooling(2, 2))
*/
//pooling6  16*29*29 ---------  16*14*14
void cnn::forward6()
{
    double maxm[2];
    for(int t=0; t<16; ++t)
    {
            for(int i=0; i<14; ++i)
            {
                    for(int j=0; j<14; ++j)
                    {
                            maxm[0] = max(conv4relu5[t][2*i][2*j],conv4relu5[t][2*i][2*j+1]);
                            maxm[1] = max(conv4relu5[t][2*i+1][2*j],conv4relu5[t][2*i+1][2*j+1]);
                            pooling6[t][i][j] = max(maxm[0],maxm[1]);
                    }
            }
    }
}

/*
--model:add(nn.SpatialConvolution(16, 16, 3, 3, 1, 1, 1))
--model:add(nn.ReLU())
*/
// conv7 and relu8 16*14*14 -------- 16*12*12
void cnn::forward78()
{
    for(int t=0; t<16; ++t)
    {
            for(int i=0; i<12; ++i)
            {
                    for(int j=0; j<12; ++j)
                    {
                            conv7relu8[t][i][j] = 0;
                            for(int f=0; f<16; ++f)
                            {
                                    for(int m=0; m<3; ++m)
                                    {
                                            for(int n=0; n<3; ++n)
                                            {
                                                    conv7relu8[t][i][j] += pooling6[f][i+m][j+n] * conv7Weight[t][f][m][n];
                                            }
                                    }
                            }
                            conv7relu8[t][i][j] += conv7Bias[t];
                            conv7relu8[t][i][j] = relu(conv7relu8[t][i][j]);
                    }
            }
    }
}

/*
--model:add(nn.SpatialMaxPooling(2, 2))
*/
//pooling9  16*12*12 ---------  16*6*6
void cnn::forward9()
{
    double maxm[2];
    for(int t=0; t<16; ++t)
    {
            for(int i=0; i<6; ++i)
            {
                    for(int j=0; j<6; ++j)
                    {
                            maxm[0] = max(conv7relu8[t][2*i][2*j],conv7relu8[t][2*i][2*j+1]);
                            maxm[1] = max(conv7relu8[t][2*i+1][2*j],conv7relu8[t][2*i+1][2*j+1]);
                            pooling9[t][i][j] = max(maxm[0],maxm[1]);
                    }
            }
    }
}

/*
--model:add(nn.Reshape(16*6*6))
*/
//reshape 10
void cnn::forward10()
{
	int idx = 0;
        for(int t=0; t<16; ++t)
	{
                for(int i=0; i<6; ++i)
		{
                        for(int j=0; j<6; ++j)
			{
                                reshape10[idx++] = pooling9[t][i][j];

                                //printf("%lf\t", pooling9[t][i][j]);
			}
		}
	}
}
/*
--model:add(nn.Linear(16*6*6, 8))
*/
//linear11 16*6*6 - ------ 8
void cnn::forward11()
{
        for(int t=0; t<8; ++t)
	{
                linear11[t] = 0;
                for(int f=0; f<576; ++f)
		{
                        linear11[t] += reshape10[f] * linear11Weight[t][f];
		}
                linear11[t] += linear11Bias[t];
                //printf("%lf\t", linear11[t]);
	}
}
#endif

