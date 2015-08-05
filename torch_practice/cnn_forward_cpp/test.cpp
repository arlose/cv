#include "cnn.h"
#include <iostream>
#include <sstream>
#include <string>
#include <iomanip>

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
	// load the cnn model
	cnn food;
	food.loadModel("./models/train.txt");

	// forward the cnn
	stringstream ss;
	string filename;
	Mat img;
        for(int idx = 1; idx <= 99; ++idx)
	{
		ss.clear();
                ss<<"./img/"<<argv[1]<<"_"<<idx<<".jpg";
		ss>>filename;
		img = imread(filename);
                if(img.empty())
                    return 1;
		food.getImg(img);//push the img to cnn
                Soutput out = food.forward();
                cout<<idx<<" : "<<out.idx<<endl;//get the result
                //for(int i=0;i<8;i++)
                //    cout<<out.score[i]<<"    ";
                 //cout<<endl;
	}

	return 0;
}
