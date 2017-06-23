import ast
from PIL import Image, ImageColor
from  qrtools import QR

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
