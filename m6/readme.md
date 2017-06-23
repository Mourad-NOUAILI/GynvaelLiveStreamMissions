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
