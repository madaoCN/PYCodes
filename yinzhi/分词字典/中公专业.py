#coding=utf8
#!/usr/bin/python
import os
import codecs
import requests
from requests import Request, Session
from bs4 import BeautifulSoup

BASEURL = 'http://zw.offcn.com/'
session = Session()
positionSet = set()
def downUrlRetrieve(url):
	'''
	下载URL
	'''
	print "downloading with requests"
	try:
		header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
				   'Accept': '''*/*''',
				   'Connection': 'keep-alive',
				   'Content-Type': 'application/x-www-form-urlencoded',
				   'Accept-Language': 'zh-CN,zh;q=0.8',
				   }
		prepare = Request('GET', url, headers=header).prepare()
		result = session.send(prepare, timeout=10)
		return result.text
	except Exception,e :
		print e
		print '下载出错了..' 
		
def getPosition(content):
	soup = BeautifulSoup(content, 'lxml')
#	table = soup.find('table', {'class':'bjbmtab'})
	for a in soup.find_all('a'):
		print '====='
		print a.text
		positionSet.add(a.text.strip())
		
def main():
	content = downUrlRetrieve('http://zw.offcn.com/gj/2016/zhuanye.html')
	soup = BeautifulSoup(content, 'lxml')
#	获取地区列表
	areaList = []
	for a in soup.find_all('a'):
		print a.text.strip()
		positionSet.add(a.text.strip())
	print len(positionSet)
	
	tragetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'mayor.txt')
	with codecs.open(tragetPath, 'w+', encoding='utf8') as file:
		for item in positionSet:
			file.write(item)
			file.write('\n')
		
		
		
		

if __name__ == "__main__":
	main()
	
