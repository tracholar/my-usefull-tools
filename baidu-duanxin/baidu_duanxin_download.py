# coding:utf-8
# download message from baidu yun 
# It is usefull when your message number is exceed 20000.
# In this case, baidu yun will refuse your sync your phone with baidu yun.
#
import urllib
import urllib2
import json

opener = urllib2.build_opener()
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh,en-US;q=0.8,en;q=0.6,zh-TW;q=0.4',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':open('cookie','rb').read(), # set your self baidu cookie to file `cookie` 
'Host':'duanxin.baidu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
}


url_tmp = r'https://duanxin.baidu.com/server/message.php?method=list&app_id=20&limit=%s'
page = '0-1000'
i = 0
nrow = 1000

f = open('data.csv','wb')
sepA = str(chr(1))
sepB = str(chr(2))
head = None
while page is not None:
	
	url = url_tmp % page
	req = urllib2.Request(url, None, headers)
	data = urllib2.urlopen(req).read()
	resp = json.loads(data)
	
	if i == 0:  # head
		head = resp['list'][0].keys()
		f.write(sepB.join(head) + sepA)
		
	for msg in resp['list']:
		msg['imei'] = msg['imei'][0]  #imei is an array
		row = []
		for it in head:
			if it in msg:
				row.append('%s' % msg[it])
			else:
				row.append('')
		row = sepB.join(row) + sepA
		f.write(row.encode('utf-8','ignore'))
		
	
	n_count = resp['total_cnt']
	i += 1
	if i*nrow > n_count:
		page = None
	else:
		page = '%d-%d' % (i*nrow, (i+1)*nrow)
		print 'fetch %s ' % page
f.close()


	
