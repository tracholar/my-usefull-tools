import os,sys
from os.path import join, getsize


def getDirSize(dir, cb, deepth = 0):
	size = 0
	if not os.path.isdir(dir):
		return size
		
	try:
		lists = os.listdir(dir)
	except Exception:
		sys.stderr.write('List ' + dir + 'Exception\n')
		return size
		
	dirs = [d for d in lists if d not in ('.','..') and os.path.isdir(join(dir, d))]
	fs = [d for d in lists if d not in ('.','..') and not os.path.isdir(join(dir, d))]
	
	for f in fs:
		p = join(dir, f)
		try:
			s = getsize(p)
		except Exception:
			s = 0
			sys.stderr.write('Getsize of' + p + 'Exception\n')
			
		cb((p, s, deepth))
		size += s
		
	for d in dirs:
		path = join(dir,d)
		s = getDirSize(path, cb, deepth+1)
		
		size += s
		cb((path,s, deepth))
	
	return size
	
def Print(data, t=0, d=10000):
	path, size, depth = data
	if size > t*1024*1024 and depth<d:
		print '%s\t\t%dMB' % (path, size/1024.0/1024.0)
if __name__ == '__main__':
	if len(sys.argv)<2:
		print 'error'
	else:
		if len(sys.argv)>=3:
			sizes = getDirSize(sys.argv[1], \
				lambda x: Print(x,int(sys.argv[2])))
		else:
			sizes = getDirSize(sys.argv[1], Print)
		print '\nAll size\t%fMB' % (sizes/1024.0/1024.0)
		
	