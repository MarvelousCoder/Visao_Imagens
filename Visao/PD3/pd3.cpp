#include <opencv2/opencv.hpp>
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

using namespace cv;
using namespace std;

int main () {
    Mat aloeL = imread("data/aloeL.png", -1);
    Mat aloeR = imread("data/aloeR.png", -1);
    Mat babyL = imread("data/babyL.png", -1);
    Mat babyR = imread("data/babyR.png", -1);
    // Size imageSize = aloeL.size(); 
    // pair.create(imageSize.height, imageSize.width * 2, CV_8UC3);

    // Mat disp(aloeL.rows, aloeR.cols, CV_8UC3);
    // Mat vdisp = disp.clone();
    Mat disp, vdisp;
    int w;
    cin >> w;
    if(w % 2 == 0) return printf("Tamanho do bloco w invalido. W precisa ser impar!\n"), 0;

    // Ptr<StereoBM> stereo = StereoBM::create(0, w);
    cv::Ptr<cv::StereoSGBM> stereo = cv::StereoSGBM::create(
        -64, 128, 7, 100, 1000, 32, 0, 15, 1000, 16, cv::StereoSGBM::MODE_HH);
    // babyL.convertTo(babyL, CV_8UC1);
    // babyR.convertTo(babyR, CV_8UC1);
    
    cvtColor(babyL, babyL, COLOR_BGR2GRAY);
    cvtColor(babyR, babyR, COLOR_BGR2GRAY);
    stereo->compute(babyL, babyR, disp);

    double min, maxi;
    minMaxIdx(disp, &min, &maxi);
    cout << min << endl << maxi << endl;
    // vdisp = (disp - min) * (255/(maxi - min));
    // minMaxIdx(vdisp, &min, &maxi);
    // cout << min << endl << maxi << endl;
    normalize(disp, vdisp, 0, 255, cv::NORM_MINMAX, CV_8UC1);
    imshow("vdisp", vdisp);
    waitKey(0);

    // Mat Q;
    // Q.at<double>(0,0)=1.0;
    // Q.at<double>(0,1)=0.0;
    // Q.at<double>(0,2)=0.0;
    // Q.at<double>(0,3)=-160.0; //cx
    // Q.at<double>(1,0)=0.0;
    // Q.at<double>(1,1)=1.0;
    // Q.at<double>(1,2)=0.0;
    // Q.at<double>(1,3)=-160.0;  //cy
    // Q.at<double>(2,0)=0.0;
    // Q.at<double>(2,1)=0.0;
    // Q.at<double>(2,2)=0.0;
    // Q.at<double>(2,3)=3740.0;  //Focal
    // Q.at<double>(3,0)=0.0;
    // Q.at<double>(3,1)=0.0;
    // Q.at<double>(3,2)=1.0/160.0;    //1.0/BaseLine
    // Q.at<double>(3,3)=0.0;    //cx - cx'

    
    Mat depth(disp.rows, disp.cols, CV_32SC1);
    for(int j=0; j<disp.cols; j++) 
    {
        for (int i=0; i<disp.rows; i++)
        {
            int intensity = (int)disp.at<uchar>(Point(j, i));
            if(intensity != 0) depth.at<int>(Point(j, i)) = 3740*160/intensity; 
            else depth.at<int>(Point(j, i)) = 0;
        }
    }

    minMaxIdx(depth, &min, &maxi);
    cout << min << endl << maxi << endl;
    depth = (depth - min) * (255/(maxi - min)) ;
    // normalize(depth, depth, 0, 255, cv::NORM_MINMAX, CV_8UC1);
    depth.convertTo(depth, CV_8U);
    namedWindow("depth", WINDOW_NORMAL);
    imshow("depth", depth);
    waitKey(0);



    // reprojectImageTo3D(vdisp, vdisp, Q);
    // image_3d.convertTo(image_3d, CV_8U);
    // normalize(image_3d, image_3d, 0, 255, cv::NORM_MINMAX, CV_8U);
    


    return 0;
}