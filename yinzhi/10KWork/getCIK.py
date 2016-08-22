#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import MDRules
import re
import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool,Process
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.CIK

conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.instance
secCom = conn.secCom
baseStandard = conn.baseStandard

CIKSet = set()
def praseXML():
    itemArr = []
    try:
        # namespaces = {'us-gaap': 'http://xbrl.us/us-gaap/2009-01-31'}
        # xmlDoc = ET.parse(path)
        # root = xmlDoc.getroot()

        ciks = secCom.xmltest.find({})
        for cik in ciks:
            print cik['cikNumber']
            CIKSet.add(cik['cikNumber'])

    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

def writeTofile():
    path = os.path.expanduser(r'~/Desktop/CIKs.txt')
    print path
    global CIKSet
    try:
        f = codecs.open(path, "a")
        for item in CIKSet:
            print item
            f.write(item)
            f.write('\n')
        f.close()
    except Exception,e:
        print e



# if __name__ == '__main__':

if __name__ == '__main__':
    DIR = '/Users/lixiaorong/Desktop/10k'
    # praseXML()
    string = 'www.baidu.com'
    print string[:-4] + '_pre' + string[-4:]

writeTofile()
# print 'processed ============'




