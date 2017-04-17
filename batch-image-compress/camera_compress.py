# coding:utf-8
# Author: github.com/tracholar
# Resize jpeg image to 1080p without lost exif data.
#

import os, glob
from os.path import join
from PIL import Image
import sys
import threading, thread
from multiprocessing import Pool
import argparse


def print_info(msg):
    print msg

#file_list = []
#lock = thread.allocate_lock()

def _compress_img(
                args
                ):
    src, target, max_size = args  # default 1080p
    if os.path.exists(target):
        return

    try:
        im = Image.open(src)
    except IOError:
        return

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

    print( 'Current image is %s' % \
                    (src)
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
    file_list = []
    for f in jpg_fs:
        file_list.append( (join(src, f), join(target, f), max_size) )

    pool = Pool(n_thread)
    pool.map(_compress_img, file_list)

    if subdir:
        for d in sub_dir:
            batch_compress_image(join(src, d), join(target,d),
                        max_size,
                        extend,
                        subdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('src', help='source directory')
    parser.add_argument('target', help='target directory')
    parser.add_argument('--maxsize', '-s', type=int, default=1080, help='max pixel, eg: 720 1080')
    parser.add_argument('--nthread', '-n', type=int, default=10, help='How many threads.')


    args = parser.parse_args()

    batch_compress_image(args.src, args.target, max_size=args.maxsize, n_thread=args.nthread)
    print 'Done!'
