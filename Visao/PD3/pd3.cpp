#include <opencv2/calib3d.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/ximgproc/disparity_filter.hpp>
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <map>

using namespace cv;
using namespace std;
using namespace cv::ximgproc;

int cx1, cy1, cx2, cy2;
bool clique = false;
map<int, int> cliques;

void on_mouse(int event, int x, int y, int flags, void* userdata) {
    if ( event == EVENT_LBUTTONDOWN )
        cliques.insert(make_pair(x, y));
}


int main () {
    Mat R_r(3,3, CV_64FC1), R_l(3,3, CV_64FC1);
    Mat T_r(3,1, CV_64FC1), T_l(3,1, CV_64FC1);

    R_r.at<double>(0, 0) = 0.48946344;
    R_r.at<double>(0, 1) = 0.87099159;
    R_r.at<double>(0, 2) = -0.04241701;
    R_r.at<double>(1, 0) = 0.33782142;
    R_r.at<double>(1, 1) = -0.23423702;
    R_r.at<double>(1, 2) = -0.91159734;
    R_r.at<double>(2, 0) = -0.80392924;
    R_r.at<double>(2, 1) =  0.43186419;
    R_r.at<double>(2, 2) = -0.40889007;

    T_r.at<double>(0, 0) = -614.549000;
    T_r.at<double>(1, 0) = 193.240700;
    T_r.at<double>(2, 0) = 3242.754000;

    R_l.at<double>(0, 0) = 0.70717199;
    R_l.at<double>(0, 1) = 0.70613396;
    R_l.at<double>(0, 2) = -0.03581348;
    R_l.at<double>(1, 0) = 0.28815232;
    R_l.at<double>(1, 1) = -0.33409066;
    R_l.at<double>(1, 2) = -0.89741388;
    R_l.at<double>(2, 0) = -0.64565936;
    R_l.at<double>(2, 1) =  0.62430623;
    R_l.at<double>(2, 2) = -0.43973369;

    T_l.at<double>(0, 0) = -532.285900;
    T_l.at<double>(1, 0) = 207.183600;
    T_l.at<double>(2, 0) = 2977.408000;

    Mat cam_matrix_l(3, 3, CV_64FC1), cam_matrix_r(3, 3, CV_64FC1);

    cam_matrix_l.at<double>(0, 0) = 6704.926882; // frectl
    cam_matrix_l.at<double>(0, 1) = 0.000103; // alphal
    cam_matrix_l.at<double>(0, 2) = 738.251932; // cxl
    cam_matrix_l.at<double>(1, 0) = 0.0; 
    cam_matrix_l.at<double>(1, 1) = 6705.241311; // fyl
    cam_matrix_l.at<double>(1, 2) = 457.560286; // cyl 
    cam_matrix_l.at<double>(2, 0) = 0.0;
    cam_matrix_l.at<double>(2, 1) =  0.0;
    cam_matrix_l.at<double>(2, 2) = 1.0;
    
    cam_matrix_r.at<double>(0, 0) = 6682.125964; // frectr
    cam_matrix_r.at<double>(0, 1) = 0.000101; // alphar
    cam_matrix_r.at<double>(0, 2) = 875.207200; // cxr
    cam_matrix_r.at<double>(1, 0) = 0.0; 
    cam_matrix_r.at<double>(1, 1) = 6681.475962; // fyr
    cam_matrix_r.at<double>(1, 2) = 357.700292; // cyr
    cam_matrix_r.at<double>(2, 0) = 0.0;
    cam_matrix_r.at<double>(2, 1) =  0.0;
    cam_matrix_r.at<double>(2, 2) = 1.0;

    Mat R = R_r * R_l.t();
    Mat T = T_r - R * T_l;

    // Rodrigues(R, R);
    // norm = 1114.0849568085998
    // Mat e1 = T/norm(T, NORM_L2);
    // Mat aux(3, 1, CV_64FC1); // (-Ty, Tx, 0).t()
    // aux.at<double>(0,0) = -T.at<double>(1,0); // -Ty
    // aux.at<double>(1,0) = T.at<double>(0,0); // Tx
    // aux.at<double>(2,0) = 0.0; // 0
    // Mat e2 = 1/(sqrt( T.at<double>(1,0) * T.at<double>(1,0) + T.at<double>(0,0)*T.at<double>(0,0) ) * aux);
    // Mat e3 = e1.cross(e2);

    // Mat R_rect(3, 3, CV_64FC1);
    // R_rect.at<double>(0,0) = e1.at<double>(0,0);
    // R_rect.at<double>(0,1) = e1.at<double>(0,1);
    // R_rect.at<double>(0,2) = e1.at<double>(0,2);
    // R_rect.at<double>(1,0) = e2.at<double>(0,0);
    // R_rect.at<double>(1,1) = e2.at<double>(0,1);
    // R_rect.at<double>(1,2) = e2.at<double>(0,2);
    // R_rect.at<double>(2,0) = e3.at<double>(0,0);
    // R_rect.at<double>(2,1) = e3.at<double>(0,1);
    // R_rect.at<double>(2,2) = e3.at<double>(0,2);

    Mat morpheus_l = imread("data/MorpheusL.jpg", 0);
    Mat morpheus_r = imread("data/MorpheusR.jpg", 0);
    Size image_size_l = morpheus_l.size(); 
    // Size image_size_r = morpheus_r.size();
    Mat R1, R2, P1, P2, Q;
    stereoRectify(cam_matrix_l, noArray(), cam_matrix_r, 
                    noArray(), image_size_l, R, T, R1, R2, P1, P2, Q, 0);
    bool isVerticalStereo = false;
    isVerticalStereo = fabs(P2.at<double>(1, 3)) > fabs(P2.at<double>(0, 3));
    Mat l1, l2, r1, r2, imgl, imgr;
    initUndistortRectifyMap(cam_matrix_l, noArray(), R1, P1, image_size_l, CV_16SC2, l1, l2);
    initUndistortRectifyMap(cam_matrix_r, noArray(), R2, P2, image_size_l, CV_16SC2, r1, r2);
    Mat img_r, img_l;
    remap(morpheus_l, img_l, l1, l2, INTER_LINEAR);
    remap(morpheus_r, img_r, r1, r2, INTER_LINEAR);

    cv::Mat pair;
    if (!isVerticalStereo)
      pair.create(image_size_l.height, image_size_l.width * 2, CV_8UC3);
    else
      pair.create(image_size_l.height * 2, image_size_l.width, CV_8UC3);
    if (!isVerticalStereo) {
        cv::Mat part = pair.colRange(0, image_size_l.width);
        cvtColor(img_l, part, cv::COLOR_GRAY2BGR);
        part = pair.colRange(image_size_l.width, image_size_l.width * 2);
        cvtColor(img_r, part, cv::COLOR_GRAY2BGR);
        for (int j = 0; j < image_size_l.height; j += 16)
            cv::line(pair, cv::Point(0, j), cv::Point(image_size_l.width * 2, j),
                    cv::Scalar(0, 255, 0));
    } else {
        cv::Mat part = pair.rowRange(0, image_size_l.height);
        cv::cvtColor(img_l, part, cv::COLOR_GRAY2BGR);
        part = pair.rowRange(image_size_l.height, image_size_l.height * 2);
        cv::cvtColor(img_r, part, cv::COLOR_GRAY2BGR);
        for (int j = 0; j < image_size_l.width; j += 16)
            line(pair, cv::Point(j, 0), cv::Point(j, image_size_l.height * 2),
                cv::Scalar(0, 255, 0));
    }
    imshow("rectified", pair);
    imwrite("pair.jpg", pair);
    
    imshow("imgl", img_l);
    imwrite("imgl.jpg", img_l);
    imshow("imgr", img_r);
    imwrite("imgr.jpg", img_r);
    while((char)waitKey(0) != 27);

    int max_disp = 160;
    double lambda = 8000.0;
    double sigma  = 1.5;
    double vis_mult = 1.0;
    int wsize = 9; 
    Mat left, right;
    img_l.convertTo(left, CV_8U);
    img_r.convertTo(right, CV_8U);
    
    Ptr<DisparityWLSFilter> wls_filter;
    Mat left_for_matcher, right_for_matcher;
    Mat left_disp,right_disp;
    Mat filtered_disp;
    right_for_matcher = left.clone();
    left_for_matcher = right.clone();
    Mat conf_map = Mat(left.rows, left.cols, CV_8U);
    conf_map = Scalar(255);
    double matching_time, filtering_time;

    Ptr<StereoSGBM> left_matcher  = StereoSGBM::create(0,max_disp,wsize);
    left_matcher->setP1(24*wsize*wsize);
    left_matcher->setP2(96*wsize*wsize);
    left_matcher->setPreFilterCap(63);
    left_matcher->setMode(StereoSGBM::MODE_SGBM_3WAY);
    wls_filter = createDisparityWLSFilter(left_matcher);
    Ptr<StereoMatcher> right_matcher = createRightMatcher(left_matcher);

    matching_time = (double)getTickCount();
    left_matcher->compute(left_for_matcher, right_for_matcher,left_disp);
    right_matcher->compute(right_for_matcher,left_for_matcher, right_disp);
    matching_time = ((double)getTickCount() - matching_time)/getTickFrequency();

    wls_filter->setLambda(lambda);
    wls_filter->setSigmaColor(sigma);
    filtering_time = (double)getTickCount();
    wls_filter->filter(left_disp,left,filtered_disp,right_disp);
    filtering_time = ((double)getTickCount() - filtering_time)/getTickFrequency();
    //! [filtering]
    conf_map = wls_filter->getConfidenceMap();

    namedWindow("left", WINDOW_AUTOSIZE);
    imshow("left", left);
    namedWindow("right", WINDOW_AUTOSIZE);
    imshow("right", right);

    //! [visualization]
    Mat raw_disp_vis;
    getDisparityVis(left_disp,raw_disp_vis,vis_mult);
    namedWindow("raw disparity", WINDOW_AUTOSIZE);
    imshow("raw disparity", raw_disp_vis);
    Mat disparity = left_disp.clone();
    double mini, maxi;
    minMaxIdx(left_disp, &mini, &maxi);
    disparity = (disparity - mini) * (255/(maxi - mini));
    disparity.convertTo(disparity, CV_8U);
    imshow("Mapa de disparidade", disparity);
    waitKey(0);

    Mat filtered_disp_vis;
    getDisparityVis(filtered_disp, filtered_disp_vis, vis_mult);
    namedWindow("filtered disparity", WINDOW_AUTOSIZE);
    imshow("filtered disparity", filtered_disp_vis);
    imwrite("teste2.jpg", filtered_disp_vis);
    waitKey(0);

    namedWindow("Req3", WINDOW_NORMAL);
    resizeWindow("Req3", 1000,  1000);
    while(1) {
        setMouseCallback("Req3", on_mouse);
        imshow( "Req3", filtered_disp_vis );
        if((char)waitKey(55) == 27) break;
    }


    Mat pt_1(4, 1, CV_64FC1), pt_2(4, 1, CV_64FC1);
    auto start = cliques.begin();
    int i = 0;
    while(start != cliques.end()) {
        pt_1.at<double>(0,0) = (double)start->first;
        pt_1.at<double>(1,0) = (double)start->second;
        pt_1.at<double>(2,0) = filtered_disp.at<double>(Point(start->second, start->first));
        pt_1.at<double>(3,0) = 1;
        ++start;
        
        pt_2.at<double>(0,0) = (double)start->first;
        pt_2.at<double>(1,0) = (double)start->second;
        pt_2.at<double>(2,0) = filtered_disp.at<double>(Point(start->second, start->first));
        pt_2.at<double>(3,0) = 1;
        pt_1 = Q * pt_1;
        pt_2 = Q * pt_2;
        if(i == 0) cout << "largura em mm(?): " << norm(pt_1, pt_2, NORM_L2) << endl;
        else if(i == 1) cout << "altura em mm(?): " << norm(pt_1, pt_2, NORM_L2) << endl;
        else if(i == 2) cout << "profundidade em mm(?): " << norm(pt_1, pt_2, NORM_L2) << endl;
        i++;
    }




    return 0;
}