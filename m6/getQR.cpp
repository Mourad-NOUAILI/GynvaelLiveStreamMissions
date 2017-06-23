/*
Needs: OpenCV installed
Compile: g++ -std=c++11 sol.cpp -o sol `pkg-config opencv --cflags --libs`
*/

#include <bits/stdc++.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

std::string extract_ints(std::ctype_base::mask category, std::string str, std::ctype<char> const& facet)
{
    using std::strlen;

    char const *begin = &str.front(),
               *end   = &str.back();

    auto res = facet.scan_is(category, begin, end);

    begin = &res[0];
    end   = &res[strlen(res)];

    return std::string(begin, end);
}

std::string extract_ints(std::string str)
{
    return extract_ints(std::ctype_base::digit, str,
         std::use_facet<std::ctype<char>>(std::locale("")));
}


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
