#!/usr/bin/env python
#coding=utf8
import os
import pymongo
from multiprocessing import Pool,Process
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.temp

def praseXML(path):
    print path
    try:
        # namespaces = {'us-gaap': 'http://xbrl.us/us-gaap/2009-01-31'}
        # xmlDoc = ET.parse(path)
        # root = xmlDoc.getroot()
        from lxml import etree
        tree = etree.parse(path)
        root = tree.getroot()
        nsmap = root.nsmap


        nsmap['fileName'] = os.path.basename(path)
        print nsmap
        try:
            print nsmap.pop(None)
        except Exception, e:
            print e

        consur.nameSpace.insert(nsmap)

        # for child in root:
        #     nameSpace = str(child.tag).strip('{').split('}')[0]
        #     for key in nsmap:
        #         if nsmap[key] == nameSpace:
        #             print child.tag, child.attrib

    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'



def getDirFile(dir):
    '''
    获取目录下html文档路径
    :param dir: 路径
    :return: 文档路径集合
    '''
    fileList = []
    list = os.listdir(dir)
    if len(list) > 0:
        for file in list:
            filePath = os.path.join(dir, file)
            if not os.path.isdir(filePath):  # 如果是不是目录,是文件
                fileList.append(filePath)

    return fileList

if __name__ == '__main__':
    DIR = '/Users/lixiaorong/Desktop/10k'
    pool = Pool(5)

    def func(args,dire,fis):
        fileList = getDirFile(dire)
        if fileList > 0:
            for file in fileList:

                if os.path.splitext(file)[-1] == '.xml':
                    fileName = os.path.basename(file)
                    splList = fileName.split('_')
                    if len(splList) == 1:
                        pool.apply_async(praseXML, args=(file,))

    os.path.walk(DIR, func, ())
    pool.close()
    pool.join()
    print 'processed ============'


