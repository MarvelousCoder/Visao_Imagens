// Example 2-11. A complete program to read in a color video and write out the log-polar-
// transformed video

#include <../opencv2/opencv.hpp>
#include <iostream>
#include <fstream>

using namespace cv;
using namespace std;


Mat img;

void help(char** argv ) {
	std::cout << "\n"
	<< "Read in a video, write out a log polar of it\n"
	<< argv[0] <<" <path/video> <paht/video_output>\n"
	<< "For example:\n"
	<< argv[0] << " ../tree.avi ../vout.avi\n"
	<< "\nThen read it with:\n ./example_02-10 ../vout.avi\n"
	<< std::endl;
}

void onMouse(int event, int x, int y, int flags, void* userdata) {
     if ( event == EVENT_LBUTTONDOWN ) {
      Vec3b intensity = img.at< Vec3b >(y, x);
      uchar blue  = intensity[0];
      uchar green = intensity[1];
      uchar red   = intensity[2];
      
      Mat img_gry;
      cvtColor( img, img_gry, COLOR_BGR2GRAY);
      bool cinza = equal(img.begin<uchar>(), img.end<uchar>(), img_gry.begin<uchar>());

      if(!cinza) {
        cout << "Em (x,y) = (" << x << ", " << y <<
          "), onde y = coluna e x = linha temos: " << endl << "(blue, green, red) = (" <<
          (unsigned int)  blue <<
          ", " << (unsigned int)green << ", " <<
          (unsigned int)  red << ")" << endl;


          
      } else {
          cout << "Em (x,y) = (" << x << ", " << y <<
            "), onde y = coluna e x = linha temos o pixel cinza: " << endl <<
            (unsigned int) img.at<uchar>(y, x) << endl;
      }
     }
}
  

int main( int argc, char** argv ) {
  
  // if (argc != 3) { 
  //  help(argv);
  //  return 0;
  // }
    
  img = imread( argv[1], -1);

  if( img.empty() ) {
    cout << "Imagem nao encontrada!" << endl; 
    return -1;
  } 

  // cv::cvtColor( img_rgb, img_gry, cv::COLOR_BGR2GRAY);
  namedWindow( "Req1", cv::WINDOW_AUTOSIZE );


  setMouseCallback("Req1", onMouse, NULL);
  imshow( "Req1", img);
  char c = (char)waitKey(0);
  if( c == 27 ) return 0; // allow the user to break out

  return 0;
}
