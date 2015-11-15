# coding:utf-8
# Author: github.com/tracholar
# Resize jpeg image to 1080p without lost exif data.
#

import os, glob
from os.path import join
from PIL import Image
import sys


def print_info(msg):
	print msg
	
def batch_compress_image(src, target, 
				max_size = 1080,	# default 1080p
				extend = 'jpg,png,bmp',  # default extend name
				subdir = True,   # default include subdirectory
				callback = print_info
				):
				
	if not os.path.exists(src):
		callback('Error: source directory not found!')
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
		n_process += 1
		if os.path.exists(join(target, f)):
			continue
		
		try:
			im = Image.open(join(src, f))
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
			new_im.save(join(target, f), 'JPEG', exif = im.info['exif'])
		else:
			new_im.save(join(target, f))
			
		callback( 'Process %d image, left %d. Current image is %s' % \
						(n_process, n_img - n_process, join(src, f))
				)
	if subdir:
		for d in sub_dir:
			batch_compress_image(join(src, d), join(target,d),
						max_size,
						extend,
						subdir,
						callback)

if __name__ == '__main__':	
	assert(len(sys.argv)>=3)
	batch_compress_image(sys.argv[1],sys.argv[2])
	print 'Done!'