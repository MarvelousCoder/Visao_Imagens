// Example 2-11. A complete program to read in a color video and write out the log-polar-
// transformed video

#include <../opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <vector>
#include <string>

using namespace cv;
using namespace std;

#define COLOR_ROWS 80
#define COLOR_COLS 600

bool cinza = false;
int x2, y2;
// void help(char **argv);
// void pinta(Mat **img, uchar blue_clique, uchar green_clique, uchar red_clique);
// void onMouse(int event, int x, int y, int flags, void* userdata);
// void imagem(char** argv);
// void video (char **argv);


void help(char** argv ) {
	cout << "\n"
  << "Digite 2 e <path/imagem> para Req. 2 ou 4 para Req. 4\n"
  << "Por exemplo: \n"
  << argv[0] <<" 2 fruits.jpg\n" << endl;
}

void pinta(Mat** img, Vec3b intensity_clique) {
    // Mat D((*img)->rows, (*img)->cols, CV_8UC3, Scalar(blue_clique, green_clique, red_clique));

    // vector<Mat> bgr(3);
    // split(D, bgr);
    // absdiff(**img, D, E)
    // **img = D;

    for(int j=0; j<(*img)->cols; j++) 
    {
      for (int i=0; i<(*img)->rows; i++)
      {
        Vec3b intensity = (*img)->at<Vec3b>(Point(j,i));
        uchar blue  = intensity[0];
        uchar green = intensity[1];
        uchar red   = intensity[2];

        if((uint)(red) == 255 && (uint)blue == 0 && (uint)green == 0) continue;
        if(norm(intensity_clique, intensity, NORM_L2) < 13) (*img)->at<Vec3b>(Point(j,i)) = {0, 0, 255};


        // uint square = (uint)(blue_clique - blue)*(uint)(blue_clique - blue) + 
        //   (uint)(red_clique - red)*(uint)(red_clique - red) + 
        //   (uint)(green_clique - green)*(uint)(green_clique - green);
        // if((square*square) < 169)
        //     (*img)->at<Vec3b>(Point(j,i)) = {0, 0, 255};
      }
    }
}

void pinta2(Mat* img, Vec3b intensity_clique) {
    // Mat D((*img)->rows, (*img)->cols, CV_8UC3, Scalar(blue_clique, green_clique, red_clique));

    // vector<Mat> bgr(3);
    // split(D, bgr);
    // absdiff(**img, D, E)
    // **img = D;

    for(int j=0; j<(*img).cols; j++) 
    {
      for (int i=0; i<(*img).rows; i++)
      {
        Vec3b intensity = (*img).at<Vec3b>(Point(j,i));
        uchar blue  = intensity[0];
        uchar green = intensity[1];
        uchar red   = intensity[2];

        if((uint)(red) == 255 && (uint)blue == 0 && (uint)green == 0) continue;
        if(norm(intensity_clique, intensity, NORM_L2) < 13) (*img).at<Vec3b>(Point(j,i)) = {0, 0, 255};


        // uint square = (uint)(blue_clique - blue)*(uint)(blue_clique - blue) + 
        //   (uint)(red_clique - red)*(uint)(red_clique - red) + 
        //   (uint)(green_clique - green)*(uint)(green_clique - green);
        // if((square*square) < 169)
        //     (*img)->at<Vec3b>(Point(j,i)) = {0, 0, 255};
      }
    }
}

void onMouse(int event, int x, int y, int flags, void* userdata) {
  if ( event == EVENT_LBUTTONDOWN ) {
    x2 = x;
    y2 = y;
    Mat* img = (Mat*) userdata;
    Vec3b intensity = img->at< Vec3b >(y, x);
    uchar blue_clique  = intensity[0];
    uchar green_clique = intensity[1];
    uchar red_clique   = intensity[2];

    if(!cinza) {

      string rgbText = "(" + to_string(x) + "," + to_string(y) +
            ") " + "=" + " [R = " + to_string(red_clique) + ", G = " + 
            to_string(green_clique) + ", B = " + to_string(blue_clique) + "]";

      Scalar textColor;

      Mat colorArray;
      colorArray = Mat(COLOR_ROWS, COLOR_COLS, CV_8UC3, Scalar(blue_clique,green_clique,red_clique));
      putText(colorArray, rgbText, Point2d(20, COLOR_ROWS - 20), FONT_HERSHEY_SIMPLEX, 0.8, textColor);
      imshow("Color", colorArray);

      cout << "Em (x,y) = (" << x << ", " << y <<
        "), onde y = coluna e x = linha, temos: " << endl << "(blue, green, red) = (" <<
        (uint)  blue_clique <<
        ", " << (uint)green_clique << ", " <<
        (uint)  red_clique << ")" << endl;
        
    } else {
        string rgbText = "(" + to_string(x) + "," + to_string(y) +
          ") " + "=" + " [CINZA = " + to_string(img->at<uchar>(y,x)) + "]";

        Scalar textColor;

        Mat colorArray;
        colorArray = Mat(COLOR_ROWS, COLOR_COLS, CV_8UC3, Scalar(blue_clique,green_clique,red_clique));
        putText(colorArray, rgbText, Point2d(20, COLOR_ROWS - 20), FONT_HERSHEY_SIMPLEX, 0.8, textColor);
        imshow("Color", colorArray);

        cout << "Em (x,y) = (" << x << ", " << y <<
          "), onde y = coluna e x = linha, temos o pixel cinza = " <<
          (uint) img->at<uchar>(y, x) << endl;
    }
    pinta(&img, intensity);
  }
}


void imagem(char** argv) {
  Mat img = imread( argv[2], -1);
  
  if( img.empty() ) {
    cout << "Imagem nao encontrada!" << endl; 
    return;
  } 
  
  if((int)img.channels() == 1) {
    Mat img_gry;
    cvtColor( img, img_gry, COLOR_GRAY2BGR, 3);
    img_gry.copyTo(img);
    cinza = true;
  } else {
    Mat img_gry2;
    cvtColor( img, img_gry2, COLOR_BGR2GRAY);
    cinza = equal(img.begin<uchar>(), img.end<uchar>(), img_gry2.begin<uchar>());
  } 
  
  namedWindow( "Req1", WINDOW_AUTOSIZE );

  // img.at<Vec3b>(Point(j,i)) = {0, 0, 255};
  for(;;) {
    setMouseCallback("Req1", onMouse, &img);
    imshow( "Req1", img);
    char c = (char)waitKey(33);
    if( c == 27 ) break; // allow the user to break out
  }
}

void video (char **argv) {
  namedWindow( "Req4", WINDOW_AUTOSIZE );

  // VideoCapture capture( argv[1] );

  VideoCapture cap( 0 );
  if (!cap.isOpened()) {
    cout << "Error opening VideoCapture." << endl;
    return;
  }
  
  Size size(
    (int)cap.get( CV_CAP_PROP_FRAME_WIDTH ),
    (int)cap.get( CV_CAP_PROP_FRAME_HEIGHT )
  );

  double FPS = cap.get(CV_CAP_PROP_FPS);
  VideoWriter out("output.mp4", CV_FOURCC('M','J','P','G'), FPS, size);
  
  Mat frame, frame_out;
  
  // Mat snapshot = Mat(frame.size(), CV_8UC3, Scalar(0,0,0));


  for(;;) {
    cap >> frame;
    if( frame.empty() ) break; // end if done

    // imshow( "Req4", frame );
    setMouseCallback("Req4", onMouse, &frame);
    pinta2(&frame, frame.at< Vec3b >(y2, x2));

    if((char)waitKey(1000.0/FPS) == 27) break;
    imshow( "Req4", frame );

  }
  cap.release();
}

int main( int argc, char** argv ) {
  
  if (argc < 2) {
    help(argv);
    return 0;
  }

  if(*argv[1] == '2')
    imagem(argv);
  else if(*argv[1] == '4') 
    video(argv);
  else help(argv);

  return 0;
}
