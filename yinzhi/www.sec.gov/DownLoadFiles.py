#coding=utf8
import requests
from requests import Session, Request
import pymongo
from multiprocessing import Pool,Process
import time
import re
import MDCompressFile
import os

BASE_URL = 'https://www.sec.gov/Archives/edgar/monthly/'
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.secCom


def downUrlRetrieve(dirName, url, fileName, files):
    '''
    下载URL
    '''
    print "downloading with requests"
    try:
        r = requests.get(url)
        fileDir = os.path.join(os.path.expanduser("/"),'home','XBRL', '%s' % dirName)
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
            print '创建目录。。', fileDir
        desktopPath = os.path.join(fileDir, fileName)
        with open(desktopPath, "wb") as code:
            code.write(MDCompressFile.gzip_compress(r.content))
            # print '当前目录数为', dirCount
            print  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
            print '写入文件-------------' , desktopPath
            # code.write(r.content)
    except Exception,e :
        print e
        print "+++++++++++++++++++++++++++++++++++++"
        # consur.fail.insert(files)
        print '错误!插入数据库'



pool = Pool(5)
noFiles = 0
itemCount = 0
# dirCount = 0
import codecs
with codecs.open('unDownload.txt') as file:
    for f in file.readlines():
        list = f.split('_')
        if len(list) == 2:
            cik = list[0].encode('utf8')
            acceptanceDateTime = list[-1].strip().encode('utf8')

            # print {'cikNumber':cik, 'acceptanceDatetime':acceptanceDateTime}

            for path in consur.rssInfo.find({'cikNumber':cik,'acceptanceDatetime':acceptanceDateTime}):
                try:
                    files = path['files']
                    # print files
                    for file in files:
                        itemCount += 1
                        suff = file['fileName'].split('.')[-1]
                        if  suff == 'xml' or suff =='xsd' or suff == 'cal' or suff == 'lab' or suff == 'pre':
                            pool.apply_async(downUrlRetrieve, args=(path['acceptanceDatetime']+'#'+ path['cikNumber'].strip(' DE '),file['url'],file['fileName'], files))

                except Exception ,e:
                    print e
                    print '不存在files数据项'
                    noFiles += 1

pool.close()
pool.join()

print noFiles, itemCount
