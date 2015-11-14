import os,sys
from os.path import join, getsize

def getdirsize(dir):
	size = 0L
	for root, dirs, files in os.walk(dir):
		size += sum([getsize(join(root, name)) for name in files])
	return size

def getDirListSize(dir, cb):
	size = []
	for root,dirs,files in os.walk(dir):
		break
	
	for d in dirs:
		path = join(root,d)
		try:
			s = getdirsize(path)
		except Exception:
			print path,'exception'
			s = 0
		size += [(path, s)]
		cb((d,s))
	
	for f in files:
		path = join(root,f)
		s = getsize(path)
		size += [(path, s)]
		cb((f,s))
	return size
	
def Print(data, t=0):
	path, size = data
	if size > t*1024*1024:
		print '%s\t\t%dMB' % (path, size/1024.0/1024.0)
if __name__ == '__main__':
	if len(sys.argv)<2:
		print 'error'
	else:
		if len(sys.argv)>=3:
			sizes = getDirListSize(sys.argv[1], \
				lambda x: Print(x,int(sys.argv[2])))
		else:
			sizes = getDirListSize(sys.argv[1], Print)
		print '\nAll size\t%fMB' % (sum([s for (t,s) in sizes])/1024.0/1024.0)
		
	