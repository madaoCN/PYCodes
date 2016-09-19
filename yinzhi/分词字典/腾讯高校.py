#coding=utf8
#!/usr/bin/python
import os
import codecs
import requests
from requests import Request, Session
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui

BASEURL = 'http://data.edu.qq.com/college/total_major.shtml?page='
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
	print soup
	print 'soup====='
#	table = soup.find('table', {'class':'co_link01'})
#	for a in table.find_all('a',{'target':'_blank'}):
#		print '====='
#		print a.text
#		positionSet.add(a.text.strip())
		
def main(args, dire, files):
	print('r')
#	cap = webdriver.DesiredCapabilities.PHANTOMJS
#	cap["phantomjs.page.settings.resourceTimeout"] = 10
#	cap["phantomjs.page.settings.loadImages"] = False
	
#	driver = webdriver.PhantomJS()
#	wait = ui.WebDriverWait(driver,10) 
#	for idx in range(1, 83):
##		content = downUrlRetrieve(BASEURL + unicode(idx))
#		driver.get(BASEURL + unicode(idx))
#		driver.implicitly_wait(10)
#		content = driver.page_source.encode('utf8','ignore')
##		getPosition(content)
#		tragetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'mayor')
#		if not os.path.exists(tragetPath):
#			os.makedirs(tragetPath)
#		with codecs.open(tragetPath + '/%s.html'%idx, 'w+') as file:
#			file.write(content)
#			print tragetPath
		
#	print(len(positionSet))
#	
#	for file in files:
#		if file.endswith('.DS_Store'):
#			continue
#		targetPath = os.path.join(dire, file)
#		print targetPath
#		file = codecs.open(targetPath, 'r+')
#		getPosition(file.read())
#		print(len(positionSet))
#	tragetPath = os.path.join(os.path.expanduser('~'), 'Desktop', '	1.')
#	with codecs.open(tragetPath, 'w+', encoding='utf8') as file:
#		for item in positionSet:
#			file.write(item)
#			file.write('\n')
		
		
		
		

if __name__ == "__main__":
	path = '/Users/liangxiansong/Desktop/mayor'
#	os.path.walk(path, main, ())
	tragetPath = os.path.join(os.path.expanduser('~'), 'Desktop', u'伦理学.txt')
	with codecs.open(tragetPath, 'r+', encoding='utf8') as file:
		for line in file.readlines():
			print line.strip().split('\t')[2]
#		for item in positionSet:
#			file.write(item)
#			file.write('\n')

	
