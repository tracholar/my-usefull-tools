#coding:utf-8
# 百度百科爬虫
import urllib, urllib2, re, smtplib, urlparse
from lxml import etree
from StringIO import StringIO
from email.mime.text import MIMEText
import threading, time
import request

def get_dom_from_string(html):
	try:
		tree = etree.parse(StringIO(html), etree.HTMLParser())
	except Exception:
		tree = etree.parse(StringIO(''), etree.HTMLParser())
	return tree

def dom_to_html(elem):
	return etree.tostring(elem, pretty_print=True)

def dom_text_content(elem):
	return re.sub(r'\s+', '-', etree.tostring(elem, method='text',encoding='unicode').strip())




visited_urls = set()
to_visited_urls = set()

def save_url(url):
	f = open('urls.txt','a')
	f.write(url + '\n')
	f.close()

def get_visited_urls():
    if os.path.exists('urls.txt'):
        return set(open('urls.txt').read().split('\n'))
    else:
        return set()

# 初始值
visited_urls = get_visited_urls()

def match_url(url):
    pat = [
        r'http://baike\.baidu\.com/.*',
        r'http://baike\.baidu\.com/item/.*'
    ]
    if url
