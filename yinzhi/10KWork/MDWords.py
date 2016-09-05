#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import re
import chardet
from multiprocessing import Pool,Process
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import codecs


def normalize(path):
    try:
        # from lxml import etree
        # tree = etree.parse(path)
        # root = tree.getroot()
        # nsmap = root.nsmap
        # print nsmap
        with codecs.open(path, 'r+', 'utf8') as file:
            content = file.read()
            result = re.search(r'<xbrl.+?>', content)
            if result:
               nameSpace = result.group(0)
               modifyed = nameSpace.replace('xbrl:', 'xmlns:')
               modifyed = re.sub(r'<xbrl.+>', modifyed, content, count=1)
               writeFile(path, modifyed)
               print 'SUCCESS'
            else:
                print 'NOT FOUND'
    except Exception, e:
        print 'error occur:'
        print e

def writeFile(path, content):
    with codecs.open(path, 'wb+', 'utf8') as file:
        file.write(content)
        print 'WRITE TO FILE' + path


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
    DIR = os.path.join(os.path.expanduser("~"), 'Desktop', 'GET')
    print DIR

    pool = Pool(5)
    def func(args,dire,fis):
        fileList = getDirFile(dire)
        if fileList > 0:
            for file in fileList:
                if os.path.splitext(file)[-1] == '.xml':
                    fileName = os.path.basename(file)
                    pool.apply_async(normalize, args=(file,))

    os.path.walk(DIR, func, ())
    pool.close()
    pool.join()
    print 'processed ============'

