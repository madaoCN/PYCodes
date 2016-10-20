#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import re
import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool,Process

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
secCom = conn.test

CIKSet = set()
def praseXML():
    itemArr = []
    try:
        # ciks = secCom.test.find({'formType':{'$regex':'10.K.+'}})
        ciks = secCom.test.find({'formType':'10-K'})
        for cik in ciks:
            fakePath = cik['cikNumber'] + '#' + cik['period'] + '#' + cik['acceptanceDatetime']
            # print fakePath
            if fakePath in CIKSet:
                print cik['cikNumber'] + '#' + cik['period'] + '#' + cik['acceptanceDatetime']
            CIKSet.add(fakePath)
        print len(CIKSet)
    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

def writeTofile():
    path = os.path.expanduser(r'~/Desktop/CIKs.txt')
    print path
    global CIKSet
    try:
        f = codecs.open(path, "w")
        for item in CIKSet:
            # print item
            f.write(item)
            f.write('\n')
        f.close()
    except Exception,e:
        print e


if __name__ == '__main__':
    praseXML()
    writeTofile()
    print 'processed ============'




