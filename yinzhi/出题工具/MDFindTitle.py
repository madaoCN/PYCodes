#!/usr/bin/env python
#coding=utf8

import os
import codecs
import re
from  bs4 import BeautifulSoup

resultSet = []

def getDirs(dir, func, arg):
    '''
    递归目录
    '''
    os.path.walk(dir, func, arg)

def ls(arg, dirname, files):
    '''
    打印路径
    '''
    print dirname, 'has the files', files


def getTitle(xmlPath):
    try:
        print '============================='
        print '开始解析'
        print xmlPath
        file = codecs.open(xmlPath, encoding='utf8')
        content =file.read()
        title = re.search('document.title=.*?;',content).group(0)
        if title:
            print '开始写文件'
            print title
            title = title.split(' ')
            title = title[-3] + ' ' +title[-1].strip('\';')
            # writeFile = codecs.open(xmlPath.replace('.html', '.txt'), 'w+',encoding='utf8')
            # writeFile.write(title)
            resultSet.append(title.encode('utf8'))
    except Exception, e:
        print 'error at dealWithXML-getTitle'
        print xmlPath
        print e




if __name__ == '__main__':
    DIR = '/Users/liangxiansong/Desktop/ckfg-data'

    def func(args,dire,files):
        for file in files:
            if file.endswith('.html'):
                getTitle(os.path.join(dire, file))

    os.path.walk(DIR, func, ())
    print len(resultSet)

    writeFile = codecs.open(os.path.join(DIR, u'目录.txt'), 'w+')
    for item in resultSet:
        writeFile.write(item)
        writeFile.write('\n')
    print 'process ============'