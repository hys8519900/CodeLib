#利用os.path和hashlib遍历目录计算所有文件的md5值
#from http://bbs.chinaunix.net/thread-1854992-1-1.html

#-*- encoding=uft-8 -*-
import io
import sys
import hashlib
import string
import os

def calMd5(afile):
    m = hashlib.md5()
    file = io.FileIO(afile,'r')
    bytes = file.read(1024)
    while(bytes != b''):
        m.update(bytes)
        bytes = file.read(1024)
    file.close()
    md5value = m.hexdigest()
    return md5value

def visitor(args, directoryName, filesInDirectory):
    print "\t"*(args-1),directoryName
    for fname in filesInDirectory:
        fpath = os.path.join(directoryName, fname)
        if not os.path.isdir(fpath):
            print "\t"*args,fname,"\t",calMd5(fpath)

def calDirMd5(startDir, level):
    os.path.walk(startDir, visitor, level+1)

if __name__ == '__main__':
    root = raw_input("type root directory: ")
    calDirMd5(root,0)
