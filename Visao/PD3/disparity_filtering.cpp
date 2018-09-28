#include <opencv2/calib3d.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/ximgproc/disparity_filter.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace cv::ximgproc;
using namespace std;

Rect computeROI(Size2i src_sz, Ptr<StereoMatcher> matcher_instance);

const String keys =
    "{help h usage ? |                  | print this message                                                }"
    "{@left          |data/aloeL.jpg    | left view of the stereopair                                     }"
    "{@right         |data/aloeL.jpg    | right view of the stereopair                                   }"
    "{dst_path       |None              | optional path to save the resulting filtered disparity map        }"
    "{dst_raw_path   |None              | optional path to save raw disparity map before filtering          }"
    "{algorithm      |bm                | stereo matching method (bm or sgbm)                               }"
    "{no-display     |                  | don't display results                                             }"
    "{no-downscale   |                  | force stereo matching on full-sized views to improve quality      }"
    "{dst_conf_path  |None              | optional path to save the confidence map used in filtering        }"
    "{vis_mult       |1.0               | coefficient used to scale disparity map visualizations            }"
    "{max_disparity  |160               | parameter of stereo matching                                      }"
    "{window_size    |-1                | parameter of stereo matching                                      }"
    "{wls_lambda     |8000.0            | parameter of post-filtering                                       }"
    "{wls_sigma      |1.5               | parameter of post-filtering                                       }"
    ;

int main(int argc, char** argv)
{
    CommandLineParser parser(argc,argv,keys);
    parser.about("Disparity Filtering Demo");
    if (parser.has("help"))
    {
        parser.printMessage();
        return 0;
    }

    String left_im = parser.get<String>(0);
    String right_im = parser.get<String>(1);

    String dst_path = parser.get<String>("dst_path");
    String dst_raw_path = parser.get<String>("dst_raw_path");
    String dst_conf_path = parser.get<String>("dst_conf_path");
    String algo = parser.get<String>("algorithm");
    bool no_display = parser.has("no-display");
    bool no_downscale = parser.has("no-downscale");
    int max_disp = parser.get<int>("max_disparity");
    double lambda = parser.get<double>("wls_lambda");
    double sigma  = parser.get<double>("wls_sigma");
    double vis_mult = parser.get<double>("vis_mult");

    int wsize;
    if(parser.get<int>("window_size") >= 0) //user provided window_size value
        wsize = parser.get<int>("window_size");
    else
    {
        if(algo=="sgbm")
            wsize = 3; //default window size for SGBM
        else if(!no_downscale && algo=="bm")
            wsize = 7; //default window size for BM on downscaled views (downscaling is performed only for wls_conf)
        else
            wsize = 15; //default window size for BM on full-sized views
    }

    if (!parser.check())
    {
        parser.printErrors();
        return -1;
    }

    //! [load_views]
    Mat left  = imread(left_im ,IMREAD_COLOR);
    if ( left.empty() )
    {
        cout <<"Cannot read image file: "<< left_im;
        return -1;
    }

    Mat right = imread(right_im,IMREAD_COLOR);
    if ( right.empty() )
    {
        cout << "Cannot read image file: " << right_im;
        return -1;
    }
    //! [load_views]
    Mat left_for_matcher, right_for_matcher;
    Mat left_disp,right_disp;
    Mat filtered_disp;
    Mat conf_map = Mat(left.rows, left.cols, CV_8U);
    conf_map = Scalar(255);
    Rect ROI;
    Ptr<DisparityWLSFilter> wls_filter;
    double matching_time, filtering_time;
    if(max_disp<=0 || max_disp%16!=0)
    {
        cout<<"Incorrect max_disparity value: it should be positive and divisible by 16";
        return -1;
    }
    if(wsize<=0 || wsize%2!=1)
    {
        cout<<"Incorrect window_size value: it should be positive and odd";
        return -1;
    }

    if(!no_downscale)
    {
        // downscale the views to speed-up the matching stage, as we will need to compute both left
        // and right disparity maps for confidence map computation
        //! [downscale]
        max_disp/=2;
        if(max_disp%16!=0)
            max_disp += 16-(max_disp%16);
        resize(left ,left_for_matcher, Size(), 0.5, 0.5);
        resize(right,right_for_matcher, Size(), 0.5, 0.5);
        //! [downscale]
    }
    else
    {
        left_for_matcher  = left.clone();
        right_for_matcher = right.clone();
    }

    if(algo=="bm")
    {
        //! [matching]
        Ptr<StereoBM> left_matcher = StereoBM::create(max_disp,wsize);
        wls_filter = createDisparityWLSFilter(left_matcher);
        Ptr<StereoMatcher> right_matcher = createRightMatcher(left_matcher);

        cvtColor(left_for_matcher,  left_for_matcher,  COLOR_BGR2GRAY);
        cvtColor(right_for_matcher, right_for_matcher, COLOR_BGR2GRAY);

        matching_time = (double)getTickCount();
        left_matcher-> compute(left_for_matcher, right_for_matcher,left_disp);
        right_matcher->compute(right_for_matcher,left_for_matcher, right_disp);
        matching_time = ((double)getTickCount() - matching_time)/getTickFrequency();
        //! [matching]
    }
    else if(algo=="sgbm")
    {
        Ptr<StereoSGBM> left_matcher  = StereoSGBM::create(0,max_disp,wsize);
        left_matcher->setP1(24*wsize*wsize);
        left_matcher->setP2(96*wsize*wsize);
        left_matcher->setPreFilterCap(63);
        left_matcher->setMode(StereoSGBM::MODE_SGBM_3WAY);
        wls_filter = createDisparityWLSFilter(left_matcher);
        Ptr<StereoMatcher> right_matcher = createRightMatcher(left_matcher);

        matching_time = (double)getTickCount();
        left_matcher-> compute(left_for_matcher, right_for_matcher,left_disp);
        right_matcher->compute(right_for_matcher,left_for_matcher, right_disp);
        matching_time = ((double)getTickCount() - matching_time)/getTickFrequency();
    }
    else
    {
        cout << "Unsupported algorithm";
        return -1;
    }

    //! [filtering]
    wls_filter->setLambda(lambda);
    wls_filter->setSigmaColor(sigma);
    filtering_time = (double)getTickCount();
    wls_filter->filter(left_disp,left,filtered_disp,right_disp);
    filtering_time = ((double)getTickCount() - filtering_time)/getTickFrequency();
    //! [filtering]
    conf_map = wls_filter->getConfidenceMap();

    // Get the ROI that was used in the last filter call:
    ROI = wls_filter->getROI();
    if(!no_downscale)
    {
        // upscale raw disparity and ROI back for a proper comparison:
        resize(left_disp,left_disp,Size(),2.0,2.0);
        left_disp = left_disp*2.0;
        ROI = Rect(ROI.x*2,ROI.y*2,ROI.width*2,ROI.height*2);
    }

    //collect and print all the stats:
    cout.precision(2);
    cout<<"Matching time:  "<<matching_time<<"s"<<endl;
    cout<<"Filtering time: "<<filtering_time<<"s"<<endl;
    cout<<endl;

    double MSE_before,percent_bad_before,MSE_after,percent_bad_after;

    if(dst_path!="None")
    {
        Mat filtered_disp_vis;
        getDisparityVis(filtered_disp,filtered_disp_vis,vis_mult);
        imwrite(dst_path,filtered_disp_vis);
    }
    if(dst_raw_path!="None")
    {
        Mat raw_disp_vis;
        getDisparityVis(left_disp,raw_disp_vis,vis_mult);
        imwrite(dst_raw_path,raw_disp_vis);
    }
    if(dst_conf_path!="None")
    {
        imwrite(dst_conf_path,conf_map);
    }

    if(!no_display)
    {
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
        imwrite("_disp.png", disparity);
        

        Mat filtered_disp_vis;
        getDisparityVis(filtered_disp, filtered_disp_vis, vis_mult);
        namedWindow("filtered disparity", WINDOW_AUTOSIZE);
        imshow("filtered disparity", filtered_disp_vis);
        //! [visualization]
        Mat depth(filtered_disp.rows, filtered_disp.cols, CV_16SC1);
        for(int j=0; j < filtered_disp.cols; j++) 
        {
            for (int i=0; i < filtered_disp.rows; i++)
            {
                short intensity = filtered_disp.at<short>(Point(j, i));
                if(intensity != 0) depth.at<short>(Point(j, i)) = 3740*160/intensity; 
            }
        }
        
        minMaxIdx(filtered_disp, &mini, &maxi);
        depth = (depth - mini) * (255/(maxi - mini));
        depth.convertTo(depth, CV_8U);
       
        namedWindow("Mapa de Profundidade", WINDOW_NORMAL);
        imshow("Mapa de Profundidade", depth);
        imwrite("_depth.png", depth);
        waitKey(0);
    }

    return 0;
}

Rect computeROI(Size2i src_sz, Ptr<StereoMatcher> matcher_instance)
{
    int min_disparity = matcher_instance->getMinDisparity();
    int num_disparities = matcher_instance->getNumDisparities();
    int block_size = matcher_instance->getBlockSize();

    int bs2 = block_size/2;
    int minD = min_disparity, maxD = min_disparity + num_disparities - 1;

    int xmin = maxD + bs2;
    int xmax = src_sz.width + minD - bs2;
    int ymin = bs2;
    int ymax = src_sz.height - bs2;

    Rect r(xmin, ymin, xmax - xmin, ymax - ymin);
    return r;
}
