/*
Needs: OpenCV installed
Compile: g++ -std=c++11 getQR.cpp -o getQR `pkg-config opencv --cflags --libs`
*/

#include <bits/stdc++.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

int  main(int argc, char const *argv[]) {
  vector<pair<int, int> > points;
  int maxX = -1, maxY = -1;

  cout <<"[+] Reading coordinates from file...\n";
  ifstream codeFile("code.txt", ios::in);

  if(codeFile) {
    string line;
    while(getline(codeFile, line)) {
      istringstream iss(line);
      int x, y;
      char ignore;
      iss >> ignore >> x >> ignore >>  y >> ignore ;
      maxX = max(maxX, x);
      maxY = max(maxY, y);
      pair<int, int> p = make_pair(x, y);
      points.push_back(p);
    }
    codeFile.close();
  }

  cout <<"[+] Creating QR code image...\n";
  Mat img(maxX+1, maxY+1, CV_8UC1, Scalar(255));
  cout <<"\tImage width: " << img.cols <<"\n";
  cout <<"\tImage height: " << img.rows <<"\n";

  vector<pair<int, int> >::iterator it;
  for (it = points.begin() ; it != points.end() ; ++it) {
    int x = it->first;
    int y = it->second;
    img.at<uchar>(y, x) = 0x00;
  }

  imwrite("qrcode.png", img);
  cout <<"\t'qrcode.png' created.\n";
  cout <<"[++END++]\n";
  return 0;
}
