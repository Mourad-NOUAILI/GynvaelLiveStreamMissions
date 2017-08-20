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

   
    
   
