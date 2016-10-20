#!/usr/bin/python
#coding=utf8

import MySQLdb as mdb
import pymongo
import requests
import os
import urllib
from bs4 import BeautifulSoup
import re
from requests import Request, Session
from multiprocessing import Pool,Process
import time
import MDCompressFile


#BASE
BASEURL = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-K&dateb=&owner=exclude&count=100'
HOMEURL = 'https://www.sec.gov'
#sesseion
# session会话
session = Session()

def downUrlRetrieve(url):
	'''
	下载URL
	'''
	print "netWorkConnecting...."
	try:
		header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
				   'Accept': '''*/*''',
				   'Connection': 'keep-alive',
				   'Content-Type': 'application/x-www-form-urlencoded',
				   'Accept-Language': 'zh-CN,zh;q=0.8',
				   }
		# prepare = Request('GET', url, headers=header).prepare()
		#
		# # index = random.randint(0, len(IPANDPORT) - 1)
		# # proxy = {'http': 'http://%s' % IPANDPORT[index].strip()}
		# # print proxy
		# result = session.send(prepare, timeout=10)
		r = requests.get(url, headers= header)

		# fileDir = os.path.join(os.path.expanduser("~"), 'Desktop','test')
		# if not os.path.exists(fileDir):
		#     os.makedirs(fileDir)
		#     print '创建目录。。', fileDir
		# desktopPath = os.path.join(fileDir, 'baike_1.html')
		# print '-------------' + desktopPath
		# with open(desktopPath, "wb") as code:
		#     # code.write(MDCompressFile.gzip_compress(r.content))
		#     code.write(r.content)
		return r.content
	except Exception,e :
		print e
		print '出错了..'
		
def praisToGetDocumentsPage(content, year):
	soup = BeautifulSoup(content, 'lxml')
	table = soup.find('table', {'summary':'Results'})
	trs = table.find_all('tr');
	for tr in trs:
		result = re.search('(20|19)\d{2}-\d{2}-\d{2}</td>', str(tr))
		if result:
			if year == result.group(0)[:4] and re.search('10.K</td>', str(tr)):#找到了匹配的年份
				aLink = tr.find('a', {'id':'documentsbutton'})
				if aLink:
					yield aLink['href']
			
#	aArr = soup.find_all('a', {'id':'documentsbutton'});
#	for a in aArr:
#		yield a['href']
#		for sibling in a.previous_siblings:
#			try:
#				yield sibling['href']#	
#			except:
#				pass
#		for sibling in a.next_siblings:
#			try:
#				yield sibling['href']#	
#			except:
#				pass
		
def praisToGetCateDocDownLink(content):
	'''
	获取分类文档下载地址
	'''
	soup = BeautifulSoup(content, 'lxml')
	aArr = soup.find_all('a')
#	cik = 'n/a'
	accepted = 'n/a'
	period = 'n/a'
	#获取cik
#	try:
#		cikTag = soup.find('div', {'id':'secNum'})
#		cik = cikTag.contents[-1].strip()
#	except:
#		pass
	#获取Accepted 和 Period
	formContent = soup.find('div', {'class':'formContent'})
	try:
		for formGrouping in formContent:
			#尝试获取formGrouping
			try:
				for div in formGrouping.find_all('div', {'class':'infoHead'}):
					divContent = div.text
					try:
						if re.search('Period', divContent):#寻找Period
							divBro = div.next_sibling.next_sibling
							if divBro:
								period = divBro.text
					except:
						pass
					try:
						if re.search('Accepted', divContent):#寻找Period
							divBro = div.next_sibling.next_sibling
							if divBro:
								accepted = divBro.text
					except:
						pass
			except:
				pass
	except:
		pass
	for a in aArr:
		try:
			link = a['href']#获取下载链接
			if re.search('\d.xml', link) or link.endswith('xsd'):
				yield (link, period, accepted)
		except:
			pass
			
def downXBRLDoc(url, cik,params):
	'''
	下载xbrl文档
	'''
	print "开始下载URL:", url
	period = params[0]
	accepted = params[1].split(' ')[0]
	try:
		content = downUrlRetrieve(url)
		fileDir = os.path.join(os.getcwd() , 'XBRLDown_1' , cik+'#'+accepted+'#'+period)
		fileName = os.path.basename(url)
		if not os.path.exists(fileDir):
			os.makedirs(fileDir)
			print '创建目录。。', fileDir
		desktopPath = os.path.join(fileDir, fileName)
		print '本地化地址-------------' , desktopPath
		print  time.strftime('%Y-%m-%d %X', time.localtime( time.time() ) )
		with open(desktopPath, "wb") as code:
			code.write(MDCompressFile.gzip_compress(content))
#			code.write(content)
	except Exception,e :
		print e
		print '出错了..'
	

def getCategoryDoc(url, cik):
	'''
	获取分类文档
	'''
	targetURL = HOMEURL + url
	content = downUrlRetrieve(targetURL)
	if content:
		for params in praisToGetCateDocDownLink(content):
			downXBRLDoc(HOMEURL+ params[0], cik,params[1:])
		
def main(cik, year):	
	content = downUrlRetrieve(BASEURL % cik)
	pool = Pool(5)
	for item in praisToGetDocumentsPage(content, year):
#		print item
		pool.apply_async(getCategoryDoc, args=(item, cik,))
	pool.close()
	pool.join()
	

if __name__ == "__main__":
	# getTheRemoteAgent()
#	main("0000320187", '2015')
	import codecs
	with codecs.open('target.txt') as file:
		for line in file.readlines():
			sp = line.strip().split('#')
			print sp[0], sp[1]
			main(sp[0], sp[1])
	