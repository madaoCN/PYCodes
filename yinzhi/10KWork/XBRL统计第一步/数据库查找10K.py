#coding=utf8
#!/usr/bin/python
import codecs
import os
import pymongo

conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
secCom = conn.secCom
rssInfo = secCom.rssInfo

if __name__ == "__main__":
	
	downSet = set()
	idx = 0
	for item in rssInfo.find({'formType':'10-K'}):
		acceptanceDatetime = item['acceptanceDatetime']
		cik = item['cikNumber']
		path = os.path.join('./', acceptanceDatetime +'#'+cik)
		print idx, path
		idx += 1
		downSet.add(path)
	
	print len(downSet)
	
	with codecs.open('/Users/liangxiansong/Desktop/10k.txt','w+', encoding='utf8') as file:
		for record in downSet:
			print '写入文件。。。。',  record
			file.write(record + '\n')

