#Python os.path.walk遍历文件，搜索文件里面的内容
#from http://www.oschina.net/code/snippet_16840_1889
#example 
#type root directory:c:
#type key:s

#result:
#c:address.py has s
#c:mine.py has s
#c:privKey_Address.py has s
#c:removeblankFromFile.py has s
#c:search_content.py has s
#Found in 5 files, visited 6

import os,sys
listonly = False
skipexts = ['.gif', '.exe', '.pyc','.o','.a','.dll','.lib','.pdb','.mdb']

def visitfile(fname, searchKey):
    global fcount, vcount
    try:
        if not listonly:
            if os.path.splitext(fname)[1] in skipexts:
                pass
            elif open(fname).read().find(searchKey) != -1:
                print '%s has %s' % (fname, searchKey)
                fcount += 1
    except: pass
    vcount += 1

def visitor(args, directoryName, filesInDirectory):
    for fname in filesInDirectory:
        fpath = os.path.join(directoryName, fname)
        if not os.path.isdir(fpath):
            visitfile(fpath, args)

def searcher(startdir, searchkey):
    global fcount, vcount
    fcount = vcount = 0
    os.path.walk(startdir, visitor, searchkey)

if __name__ == '__main__':
    root = raw_input("type root directory:")
    key = raw_input("type key:")
    searcher(root, key)
    print 'Found in %d files, visited %d' % (fcount, vcount)
