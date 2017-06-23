# Solution of the mission 6
Huffman Junior's file contains some code that seems like coordinates.

The first reflex is to draw that points on an image.

## How do solve it ?
1. Read coordinates from the file.
1. For each coordinate, draw the pixel on the image in order to get the QR code image.
1. Do a mirror transformation on the obtained image.
1. Resize it to a bigger size.
1. Decode the QR code.

### Get the image
To do that you must read some code in you favorite langage (you can use python with the PIL library, or C/C++ with openCV lib.)

