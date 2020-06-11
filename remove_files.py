import os
import glob

def remove(source, fileType):
    filelist = glob.glob(source + '/*' + fileType)
    for f in filelist:
        os.remove(f)