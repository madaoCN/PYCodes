#coding=utf8

import MySQLdb as mdb
import MDPraseDetail
import pymongo
import requests
import os
import urllib
from bs4 import BeautifulSoup
#BASE
BASURL = 'http://baike.baidu.com/search/word?word='
BAIKEURL = 'http://baike.baidu.com'
#MONGODB
mongoConn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
mongoCursor = mongoConn.zeCheng
provinceCol = mongoCursor.province
linkCol = mongoCursor.link
#MYSQL
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'Lxs123456',
    'db': 'zeCheng',
    'charset': 'utf8'
}
conn = mdb.connect(**config)
#获取游标
cursor = conn.cursor(cursorclass=mdb.cursors.DictCursor)

def insertSQL(value):
    sql = '''INSERT INTO t_BaseInfo (name,govID)
                                    values("%s",%d)''' % value
    print sql
    cursor.execute(sql)
    conn.commit()
    print '插入数据库成功...........'

# def getLinkAndArea():
#     TABLE_NAME = 't_PositionInfo'
#     sql = '''SELECT name,govID,provinceControl,cityControl,districtControl
#               FROM %s ''' % TABLE_NAME
#     print sql
#     count = cursor.execute(sql)
#     print count
#     for item in cursor.fetchall():
#         insertSQL((item['name'], item['govID']))

def getLinkAndArea():
    TABLE_NAME = 't_PositionInfo'
    sql = '''SELECT name,govID,provinceControl,cityControl,districtControl
              FROM %s ''' % TABLE_NAME
    count = cursor.execute(sql)
    print count
    # for item in cursor.fetchall():
    #     print item
    content = downUrlRetrieve(BASURL + urllib.quote(u'李军'.encode('gbk')))
    soup = BeautifulSoup(content, 'lxml')
    result = soup.find('ul', {'class':'polysemantList-wrapper cmn-clearfix'})
    if result:
        print result
    else:
        print '没有多义词'#没有多义项
        persistence(content)

def persistence(content):
    try:
        fileDir = os.path.join(os.path.expanduser("~"), 'Desktop','test')
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
            print '创建目录。。', fileDir
        desktopPath = os.path.join(fileDir, 'baike.html')
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
        r = requests.get(url)
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
    getLinkAndArea()