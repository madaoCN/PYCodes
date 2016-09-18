#coding=utf8

import MySQLdb as mdb
import MDPraseDetail
import pymongo
import requests
import os
import urllib
from bs4 import BeautifulSoup
import re
from requests import Request, Session
import time
import chardet
#BASE
BASURL = 'http://baike.baidu.com/search/word?word='
BAIKEURL = 'http://baike.baidu.com'


#sesseion
# session会话
session = Session()
# 地址列表
IPANDPORT = []
# 获取代理列表


# def getLinkAndArea():
#     TABLE_NAME = 't_PositionInfo'
#     sql = '''SELECT name,govID,provinceControl,cityControl,districtControl
#               FROM %s ''' % TABLE_NAME
#     print sql
#     count = cursor.execute(sql)
#     print count
#     for item in cursor.fetchall():
#         insertSQL((item['name'], item['govID']))

def getLinkAndArea(filePath):

    unDownLoadFile = '/Users/liangxiansong/Desktop/unDownload.txt'
    import codecs
    with codecs.open(unDownLoadFile, encoding='utf8') as file:
        idx = 0
        for row in file:
            print idx
            idx += 1
            print row.strip()
            list = row.strip('.\n').split('/')

            fileName = list[-1]
            print fileName
            name = re.search('_.*?_', fileName)
            name = name.group(0).strip('_')
            position = re.search('\..*?_', ''.join(fileName[::-1]))
            position = position.group(0).strip('._').strip()
            position = ''.join(position[::-1])

            #saveName
            saveName = os.path.basename(fileName)
            savePath = filePath +row.strip(saveName)
            content = downUrlRetrieve(BASURL + urllib.quote(name.encode('utf8')))
            soup = BeautifulSoup(content, 'lxml')
            result = soup.find('ul', {'class':'polysemantList-wrapper cmn-clearfix'})
            if result:#有多义项,需要全文检索

                print '有多义词......', len(result.find_all('li')), "项"
                searchKey = position.replace(u'长',u'.*?长').replace(u'书记',u'.*?书记')
                # searchKey = city if city != None and city != 'None' else searchKey
                # searchKey = district if district != None and district != 'None' else searchKey
                # searchKey.replace('')
                searchKey = searchKey.encode('utf8')
                print '检索字段:',searchKey

                print BASURL + urllib.quote(name.encode('utf8'))
                searchDetail = content.split('<div class="main-content">')[-1]
                if re.search(searchKey,searchDetail):
                    persistence(content, savePath, saveName)
                else:
                    print '页面里木有找到哦'
                    for li in result:
                        result = li.find('a')
                        if not isinstance(result, int) and result != None:
                            detailURL = BAIKEURL + result['href']
                            print detailURL
                            searchDetail = downUrlRetrieve(detailURL)
                            searchDetail = content.split('<div class="main-content">')[-1]
                            if re.search(searchKey, searchDetail):
                                persistence(content, savePath, saveName)
                                break
                            else:
                                print '页面里木有找到哦'
            else:
                print '没有多义词......'#没有多义项
                persistence(content, savePath, saveName)

def persistence(content, savePath, saveName):
    try:
        # fileDir = os.path.join(os.path.expanduser("~"), 'Desktop','test')
        if not os.path.exists(savePath):
            os.makedirs(savePath)
            print '创建目录。。', savePath
        desktopPath = os.path.join(savePath, saveName + '.html')
        print '-------------' + desktopPath
        with open(desktopPath, "wb") as code:
            # code.write(MDCompressFile.gzip_compress(r.content))
            code.write(content)
    except Exception,e :
        print e
        print '出错了..'

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
        # prepare = Request('GET', url, headers=header).prepare()
        #
        # # index = random.randint(0, len(IPANDPORT) - 1)
        # # proxy = {'http': 'http://%s' % IPANDPORT[index].strip()}
        # # print proxy
        # result = session.send(prepare, timeout=10)
        time.sleep(1)
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

if __name__ == "__main__":
    # getTheRemoteAgent()
    # getLinkAndArea(os.path.join(os.path.expanduser('/'), 'Volumes', 'TOSHIBA EXT', 'baike'))
    getLinkAndArea(os.path.join(os.path.expanduser('~'), 'Desktop', 'TOSHIBA EXT', 'baike'))