# coding:utf-8
# Author: github.com/tracholar
# Resize jpeg image to 1080p without lost exif data.
#

import os, glob
from os.path import join
from PIL import Image
import sys
import threading, thread


def print_info(msg):
    print msg
    
file_list = []
lock = thread.allocate_lock()

def _compress_img(
                max_size = 1080 # default 1080p
                ):
    
    while True:
        
        
        lock.acquire()
        left = len(file_list)
        
        if left == 0:
            lock.release()
            return True
            
        src, target = file_list.pop(0)
        
        lock.release()
        
        
        
        if os.path.exists(target):
            continue
        
        try:
            im = Image.open(src)
        except IOError:
            continue
            
        width, height = im.size
        
        if width < height:
            scale = 1.0 * max_size / width
        else:
            scale = 1.0 * max_size / height
        scale = min(1.0, scale)
        
        new_size = int(width * scale), int(height * scale)
        new_im = im.resize(new_size)
        
        if 'exif' in im.info:
            new_im.save(target, 'JPEG', exif = im.info['exif'])
        else:
            new_im.save(target)
            
        print( 'Left %d. Current image is %s' % \
                        (left, src)
                )
            
def batch_compress_image(src, target, 
                max_size = 1080,    # default 1080p
                extend = 'jpg,jpeg,png,bmp',  # default extend name
                subdir = True,   # default include subdirectory
                n_thread = 10     # default use 10 threads. 
                ):
                
    if not os.path.exists(src):
        print('Error: source directory not found!')
        return
        
    extends = extend.split(',')

    fs = os.listdir(src)
    jpg_fs = [f for f in fs if f not in ('.', '..') and f[-3:].lower() in extends]
    sub_dir = [f for f in fs if f not in ('.', '..') and os.path.isdir(join(src, f))]
    
    if not os.path.exists(target):
        os.mkdir(target)
    
    n_img = len(jpg_fs)
    n_process = 0
    for f in jpg_fs:
        file_list.append( (join(src, f), join(target, f)) )

    ts = []
    for i in range(n_thread):
        t = threading.Thread(target=_compress_img, args=(max_size,))
        t.start()
        ts.append(t)
        
    for t in ts:
        t.join()
        
    if subdir:
        for d in sub_dir:
            batch_compress_image(join(src, d), join(target,d),
                        max_size,
                        extend,
                        subdir)

if __name__ == '__main__':  
    assert(len(sys.argv)>=3)
    batch_compress_image(sys.argv[1],sys.argv[2])
    print 'Done!'