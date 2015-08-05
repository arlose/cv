#ifndef CNN_H
#define CNN_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <string>

using namespace std;
using namespace cv;

#define MAXLAYERNUM 40
#define MAXDIMSIZE  4

typedef struct
{
	int idx;
	double *score;
}Soutput;

typedef struct
{
	int layernumber;
	int type[MAXLAYERNUM];
	int inputdim[MAXLAYERNUM];
	int inputsize[MAXLAYERNUM][MAXDIMSIZE];
	int weightdim[MAXLAYERNUM];
	int weightsize[MAXLAYERNUM][MAXDIMSIZE];
	int biasdim[MAXLAYERNUM];
	int biassize[MAXLAYERNUM][MAXDIMSIZE];
	int outputdim[MAXLAYERNUM];
	int outputsize[MAXLAYERNUM][MAXDIMSIZE];
}SLayerInfo;

class cnn
{
	private:
		double * layer_weight[MAXLAYERNUM];
		double * layer_bias[MAXLAYERNUM];

		double * input;
		double * layer_output[MAXLAYERNUM];
		
		SLayerInfo info;

	public:
		cnn();
		~cnn();

		bool loadModel(string filename);
		bool loadModelInfo(string filename);
        	bool getImg(Mat matImg);
		Soutput forward();
};

#endif
