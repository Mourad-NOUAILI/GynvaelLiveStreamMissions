# The Gynvael's mission #7 solution
The mission: http://gynvael.vexillium.org/ext/659530fc374da060c014f6d4dd5c124040dfb458_mission007.txt

The corrupted ZIP file: https://goo.gl/RkjVaY (you can found it also [here](https://github.com/Mourad-NOUAILI/GynvaelLiveStreamMissions/blob/master/m7/ZIP-files/m7-before.zip) )

When you try to unzip the file with your favourite tool you will get an error.

I use 7z:

![DCF](/m7/images/extract-errors.png)

The content of the decompressed file (report.txt) is unreadble:

![UNR](/m7/images/extracted-wrong-file.png)


You need to get some information about the ZIP file. I use zipinfo:

![INFO1](/m7/images/zipinfo-before-change.png)

As you see, there is a compression:
```
compressed size:                                94 bytes
uncompressed size:                              122 bytes
```
But the NO compression method:
```
compression method:                             none (stored)
```
## Some notions

### Compression methods

https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html

![CM1](/m7/images/ppmd.png)


https://en.wikipedia.org/wiki/Zip_(file_format)#Compression_methods

![CM2](/m7/images/cm-wiki.png)

### The ZIP headers

https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html

![H1](/m7/images/zip-lfh.png)

![H2](/m7/images/zip-cdh.png)

## Steps to resolve the mission

As we had seen, we must change the value of the compression method from 0x0000 to one value from the list below:

* 0x0001: shrunk

* 0x0002: reduced with compression factor 1

* 0x0003: reduced with compression factor 2

* 0x0004: reduced with compression factor 3

* 0x0005: reduced with compression factor 4

* 0x0006: imploded

* 0x0007: reserved

* 0x0008: deflated

* 0x0009: enhanced deflated

* 0x000A: PKWare DCL imploded

* 0x000B: reserved

* 0x000C: compressed using BZIP2

* 0x000D: reserved

* 0x000E: LZMA

* 0x000F-0x0011: reserved

* 0x0012: compressed using IBM TERSE

* 0x0013: IBM LZ77 z

* 0x0062: PPMd version I, Rev 1 

### Step 1: Change the compression method value
Open the ZIP file with your favorite Hex Editor.

After multiple tries, We discover that the compression method used by Gynvael is: PPMd.

```You must know that the ZIP headers values are little indian.```

Before change:

![B1](/m7/images/bytes-before-change.png)

After change:

![A1](/m7/images/hex-change-byte.png)

### Step 2: ckeck it

Run zipinfo to check:

![B2](/m7/images/zipinfo-after-change.png)

### Step 3: Extract the file

![X](/m7/images/extract-the-correct-file.png)

The answer is:

![R](/m7/images/the-answer.png)

#Python code that do all the stuff

```python
import os
import zipfile
import sys

GREEN = "\033[0;32m"
RED   = "\033[1;31m" 
RESET = "\033[0;0m"

compDic = {
        '\x01': 'shrunk',
        '\x02': 'reduced with compression factor 1',
        '\x03': 'reduced with compression factor 2',
        '\x04': 'reduced with compression factor 3',
        '\x05': 'reduced with compression factor 4',
        '\x06': 'imploded',
        '\x07': 'reserved',
        '\x08': 'deflated',
        '\x09': 'enhanced deflated',
        '\x0a': 'PKWare DCL imploded',
        '\x0b': 'reserved',
        '\x0c': 'compressed using BZIP2',
        '\x0d': 'reserved',
        '\x0e': 'LZMA',
        '\x0f': 'reserved',
        '\x12': 'compressed using IBM TERSE',
        '\x13': 'IBM LZ77 z',
        '\x62': 'PPMd version I, Rev 1'
        }
  


def readAndReplaceAtOffset(f, startOffset, replacement):
    f.seek(startOffset, 0)
    f.write(bytearray(replacement, 'utf8'))
    f.seek(startOffset, 0)
    f.write(bytearray(replacement, 'utf8'))

sys.stdout.write(RED)
print ("Gynvael mission #7")
print ("Coded by Mourad NOUAILI aka blackbird")
sys.stdout.write(RESET)

if len(sys.argv) != 2:
    print("Usage: "+sys.argv[0]+" file.zip")
    sys.exit(0)

filename = sys.argv[1]
zf = zipfile.ZipFile(filename, 'r')
files = zf.namelist()


with open(filename, "rb+") as f:
    for k, v in compDic.items():
        for fi in files:
            try:
                statinfo = os.stat(fi)
                if statinfo.st_size > 0:
                    sys.stdout.write(GREEN)
                    print ("BINGO: got it :)")
                    sys.stdout.write(RESET)
                    os.system('cat '+fi)
                os.remove(fi)
            except FileNotFoundError:
                continue
        print ("[+]test with: " + v + " compression...")
        readAndReplaceAtOffset(f, 0x8, k)
        readAndReplaceAtOffset(f, 0x90, k)
        cmd = '7z x ' + filename + ' > tmp'
        os.system(cmd) 
        print
f.close()
```
## Run it
![RUN](/m7/images/run.png)
