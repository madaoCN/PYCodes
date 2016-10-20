#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import xlwt
from multiprocessing import Pool,Process
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
consur = conn.temp

def praseXML():
    try:
        items = consur.nameSpace.find()
        for item in items:
            for key in item:
                if key == '_id':
                    continue
                print key, item[key]
                target = None
                for u in consur.uniqueKey.find({},{key:'1'}):
                    target = u
                if target != None:
                    try:
                        if target[key] != None:
                            print '已存在键'
                            consur.uniqueKey.update(u, {'$addToSet': {key: item[key]}})
                    except Exception, e:
                        print '未存在'
                        consur.uniqueKey.insert({key: [item[key]]})
                        print '录入数据库'

    except Exception, e:
        print 'error++++++++++++++'
        print e
        print 'error--------------'

if __name__ == '__main__':
    DIR = '/Users/lixiaorong/Desktop/10k'
    praseXML()



