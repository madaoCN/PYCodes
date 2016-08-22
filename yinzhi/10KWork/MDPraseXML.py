#coding=utf8
import os
import lxml
from bs4 import BeautifulSoup
import pymongo
import codecs
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import chardet



__DOWNLOAD_BASE_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/downLoad/')
__XML_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/xmls/')
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.secCom
collection = consur.xmlInfo


def praseXML(path):
    try:
        # namespaces = {'us-gaap': 'http://xbrl.us/us-gaap/2009-01-31'}
        # xmlDoc = ET.parse(path)
        # root = xmlDoc.getroot()
        from lxml import etree
        tree = etree.parse(path)
        root = tree.getroot()
        nsmap = root.nsmap
        print nsmap

        for child in root:
            nameSpace = str(child.tag).strip('{').split('}')[0]
            for key in nsmap:
                if nsmap[key] == nameSpace:
                    print child.tag, child.attrib

    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e

def loadToDB(dic):
    print '录入数据库。。。。'
    try:
        consur.xmltest.insert(dic)
    except Exception,e:
        print '录入数据库失败'
        consur.fail.insert({'path':dic['source']})
        print e

if __name__ == '__main__':
    myDic =  praseXML('/Users/lixiaorong/Desktop/bdx-20090930.xml')
    print myDic
    # loadToDB(dic)











