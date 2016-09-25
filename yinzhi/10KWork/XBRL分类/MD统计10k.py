#coding=utf8
import codecs
import os
import pymongo

conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
secCom = conn.secCom
rssInfo = secCom.rssInfo

if __name__ == "__main__":

	filePath = '/Users/liangxiansong/Desktop/folder.txt'
	file = codecs.open(filePath,'r+', encoding='utf8')
	
	downSet = set()
	idx = 0
	for item in file.readlines():
		sp = item.split('#')
		acceptanceDateTime = sp[0].strip('./')
		cik = sp[-1].strip()
		print acceptanceDateTime, cik
		
		result = rssInfo.find_one({'acceptanceDatetime':acceptanceDateTime,'cikNumber':cik})
		formType = result['formType']
		if formType == "10-K":
			print idx
			idx += 1
			downSet.add(item.strip())
	
	print len(downSet)
	
	with codecs.open('/Users/liangxiansong/Desktop/10k.txt','w+', encoding='utf8') as file:
		for record in downSet:
			print '写入文件。。。。',  record
			file.write(record + '\n')

