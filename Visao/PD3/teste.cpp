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
        -64, 128, 5, 100, 1000, 32, 0, 15, 1000, 16, cv::StereoSGBM::MODE_HH);
    cvtColor(babyL, babyL, COLOR_BGR2GRAY);
    cvtColor(babyR, babyR, COLOR_BGR2GRAY);
    stereo->compute(babyL, babyR, disp);

    normalize(disp, vdisp, 0, 255, cv::NORM_MINMAX, CV_8U);
    imshow("vdisp", vdisp);
    waitKey(0);


    return 0;
}