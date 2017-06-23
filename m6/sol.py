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
