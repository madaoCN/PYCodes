#coding=utf8

import MySQLdb as mdb
import yinzhi.jiaqi.MDPraseDetail
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


def getLinkAndArea(filePath):
    downLoad = set()
    with codecs.open('/Users/liangxiansong/Desktop/needDelete.txt') as FILE:
        for line in FILE.readlines():
            os.remove(line.strip())
            os.path.abspath()



if __name__ == "__main__":
    # getTheRemoteAgent()
    # getLinkAndArea(os.path.join(os.path.expanduser('/'), 'Volumes', 'TOSHIBA EXT', 'baike'))
    getLinkAndArea('./')