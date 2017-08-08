# Solution of the mission 6
Huffman Junior's file contains some code that seems like coordinates.

The first reflex is to draw that points on an image.

## How do solve it ?
1. Read coordinates from the file.
1. For each coordinate, draw the pixel on the image in order to get the QR code image.
1. Do a mirror transformation on the obtained image.
1. Resize it to a bigger size.
1. Decode the QR code.

### Get the image (1 && 2)
#### N.B.: With python, python-pil package must be installed: https://launchpad.net/ubuntu/xenial/+package/python-pil

To do that you must read some code in you favorite langage (you can use python with the PIL library, or C/C++ with openCV lib.)
```python
import ast
from PIL import Image, ImageColor

def getPoints(filename):
    with open(filename, 'r') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    points=[]
    MAX_X = -1
    MAX_Y = -1;

    for c in content:
        c = ast.literal_eval(c)
        MAX_X = max(MAX_Y, c[0])
        MAX_Y = max(MAX_Y, c[1])
        points.append(c)

    return points, MAX_X, MAX_Y

def createQRImage(filename, points):
    im = Image.new('1', (MAX_X + 1, MAX_Y + 1), "white")
    for p in points:
        im.putpixel((p[0], p[1]), ImageColor.getcolor('black', '1'))
    im.save(filename)
    return im

print "[+] Reading coordinates from file..."
points, MAX_X, MAX_Y = getPoints("code.txt")

print"[+] Creating QR code image..."
im = createQRImage('M6-QR.png', points)
print "\t'M6-QR.png' created.";
```
#### N.B.: With c++, OpenCV must be installed: http://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html

```c++
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

```

The obtained image is 25x25 pixels size:


![QR code](M6-QR.png)

If you try do decode the image with an online QR decder for example https://webqr.com/, you will get nothing:
![error1](/m6/images/webqr-err1.png)

### Do a mirror transformation
The image may be flipped, doing a flip to the image may resolve the problem. 

Use Gimp or any Images Editor. I use Gimp:

![Mirrored QR](/m6/images/M6-QR-MIRRORED.png)


Let's try with https://webqr.com/:

![error2](/m6/images/webqr-err2.png)


### Resize the QR image
May be the QR code cound't be read because of the size.

resize it the Gimp to 400x400 pixels:

![resized](/m6/images/M6-QR-RESIZED.png)


### Decode it

![decoded](/m6/images/ANSWER.png)


## Python script to do all the stuff
### N.B.: python-qrtools package must be installed: https://code.launchpad.net/~qr-tools-developers/+archive/ubuntu/daily

```python
import ast
try:
    from PIL import Image, ImageColor
except:
    print "Pillow is not installed."
    print "python2: pip install Pillow"
    print "python3: python3 -m pip install Pillow"
    print "The solution on my github: https://github.com/Mourad-NOUAILI/GynvaelLiveStreamMissions/tree/master/m6"


try:
    from  qrtools import QR
except:
    print "qrtools not installed."
    print "sudo add-apt-repository ppa:qr-tools-developers/daily"
    print "sudo apt update"
    print "sudo apt intsall python-qrtools"
    print "The solution on my github: https://github.com/Mourad-NOUAILI/GynvaelLiveStreamMissions/tree/master/m6"


def getPoints(filename):
    with open(filename, 'r') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    points=[]
    MAX_X = -1
    MAX_Y = -1;

    for c in content:
        c = ast.literal_eval(c)
        MAX_X = max(MAX_Y, c[0])
        MAX_Y = max(MAX_Y, c[1])
        points.append(c)

    return points, MAX_X, MAX_Y

def createQRImage(filename, points):
    im = Image.new('1', (MAX_X + 1, MAX_Y + 1), "white")
    for p in points:
        im.putpixel((p[0], p[1]), ImageColor.getcolor('black', '1'))
    im.save(filename)
    return im

def resizeImage(basewidth, baseheight, oldImage, newImage):
    img = Image.open(oldImage)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)

    img.save(newImage)

print "[+] Reading coordinates from file..."
points, MAX_X, MAX_Y = getPoints("code.txt")

print"[+] Creating QR code image..."
im = createQRImage('M6-QR.png', points)
print "\t'M6-QR.png' created.";

print"[+] Vertical Mirror on QR code image..."
im.transpose(Image.FLIP_LEFT_RIGHT).save("M6-QR-MIRRORED.png")
print "\t'M6-QR-MIRRORED.png' created.";


print"[+] Resizing the QR code image..."
resizeImage(400, 400, "M6-QR-MIRRORED.png", "M6-QR-MIRRORED-RESIZED.png")

print"[+] Getting the code..."
myCode = QR(filename=u"M6-QR-MIRRORED-RESIZED.png")
if myCode.decode():
  print "\tThe code is: "+myCode.data
else:
    print "\tcan't decode QR code !!"

```

![script out put](/m6/images/script-output.png)
