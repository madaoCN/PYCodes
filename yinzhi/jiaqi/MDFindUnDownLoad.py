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
import codecs
#BASE
BASURL = 'http://baike.baidu.com/search/word?word='
BAIKEURL = 'http://baike.baidu.com'
#MONGODB
mongoConn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
mongoCursor = mongoConn.zeCheng
provinceCol = mongoCursor.province
linkCol = mongoCursor.link
baikeCol = mongoCursor.baike
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

#sesseion
# session会话
session = Session()
# 地址列表
IPANDPORT = []
# 获取代理列表

def getTheRemoteAgent():
    f = open("/Users/liangxiansong/Desktop/proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

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

def getLinkAndArea(filePath):
    TABLE_NAME = 't_PositionInfo'
    sql = '''SELECT id, name,govID,position,provinceControl,cityControl,districtControl,startDate,endDate
              FROM %s ''' % TABLE_NAME
    count = cursor.execute(sql)

    idx = 0
    allSet = set()
    for item in cursor.fetchall():
        # print idx
        idx += 1
        savePath = filePath
        name = item['name']
        # name = name.split(u'（')[0]
        province = item['provinceControl']
        city = item['cityControl']
        district = item['districtControl']
        position = item['position']
        startDate = item['startDate']
        endDate = item['endDate']
        # print item['id'],name, province, city, district, position, startDate, endDate
        saveName = startDate + '-' + endDate +'_'+name +'_'+ position
        #百科html下载存储路径
        savePath = savePath if province and province == 'None' else os.path.join(savePath, province)
        savePath = savePath if city and city == 'None' else os.path.join(savePath, city)
        savePath = savePath if district and district == 'None' else os.path.join(savePath, district)
        # print savePath+saveName+'.html'
        savePath = savePath+'/'+saveName+'.html'
        if savePath in allSet:
            print savePath
        allSet.add(savePath)

    print idx
    print 'allSet',len(allSet)

    #全集
    # allSet = set()
    # with codecs.open('/Users/liangxiansong/Desktop/all.txt') as FILE:
    #     for line in FILE.readlines():
    #         # print line.strip()
    #         allSet.add(line.strip().decode('utf8'))
    # print 'allSet', len(allSet)


    #已下载
    downLoad = set()
    with codecs.open('/Users/liangxiansong/Desktop/folder.txt') as FILE:
        for line in FILE.readlines():
            # print line.strip()
            downLoad.add(line.strip().decode('utf8'))
    print 'downSet',len(downLoad)

    resultSet = allSet - downLoad
    print 'resultSet',len(resultSet)

    filePath = os.path.join(os.path.expanduser('~'), 'Desktop','needDownload.txt')
    with codecs.open(filePath, 'w+', encoding='utf8') as file:
        for item in resultSet:
            file.write(item)
            file.write('\n')



if __name__ == "__main__":
    # getTheRemoteAgent()
    # getLinkAndArea(os.path.join(os.path.expanduser('/'), 'Volumes', 'TOSHIBA EXT', 'baike'))
    getLinkAndArea('./')