#!/usr/bin/python
# coding=utf8
import os
import lxml
from bs4 import BeautifulSoup
import pymongo
import codecs
from xml.etree import ElementTree
import pprint
import re
from multiprocessing import Pool, Process

__XML_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/xmls/')
numFile = codecs.open(os.path.join(os.path.expanduser('~'), 'Desktop', 'num.txt'), 'w+')
conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
consur = conn.test


def praseXML(path, targetFile):
    LIST = []
    try:
        xmlDoc = ElementTree.parse(path)
        root = xmlDoc.getroot()

        index = 0
        lst_node = root.getiterator("item")

        for node in lst_node:
            dic = {}
            files = []
            # 属性
            #			try:
            #				title = node.find('title').text
            #				dic['title'] = title
            #			except Exception, e:
            #				pass
            #
            #			try:
            #				link = node.find('link').text
            #				dic['link'] = link
            #			except Exception, e:
            #				pass
            #
            #			try:
            #				guid = node.find('guid').text
            #				dic['guid'] = guid
            #			except Exception, e:
            #				pass
            #
            #			try:
            #				enclosure = node.find('enclosure').attrib['url']
            #				dic['enclosure'] = enclosure
            #			except Exception, e:
            #				pass
            #
            #			try:
            #				description = node.find('description').text
            #				dic['description'] = description
            #			except Exception, e:
            #				pass
            #
            #			try:
            #				pubDate = node.find('pubDate').text
            #				dic['pubDate'] = pubDate
            #			except Exception, e:
            #				pass

            # 属性
            namespaces = {'edgar': 'http://www.sec.gov/Archives/edgar'}  # add more as needed
            xbrlFiling = node.find('edgar:xbrlFiling', namespaces)
            #			try:
            #				data = xbrlFiling.find('edgar:companyName',namespaces).text
            #				dic['companyName'] = data
            #			except Exception, e:
            #				pass

            try:
                data = xbrlFiling.find('edgar:formType', namespaces).text
                dic['formType'] = data
                if data != '10-K':
                    continue
            except Exception, e:
                pass

            # try:
            #     data = xbrlFiling.find('edgar:filingDate', namespaces).text
            #     dic['filingDate'] = data
            # except Exception, e:
            #     pass

            try:
                data = xbrlFiling.find('edgar:cikNumber', namespaces).text
                dic['cikNumber'] = data
            except Exception, e:
                pass

            # try:
            #     data = xbrlFiling.find('edgar:accessionNumber', namespaces).text
            #     dic['accessionNumber'] = data
            # except Exception, e:
            #     pass
            #
            # try:
            #     data = xbrlFiling.find('edgar:fileNumber', namespaces).text
            #     dic['fileNumber'] = data
            # except Exception, e:
            #     pass

            try:
                data = xbrlFiling.find('edgar:acceptanceDatetime', namespaces).text
                dic['acceptanceDatetime'] = data
            except Exception, e:
                pass

            try:
                data = xbrlFiling.find('edgar:period', namespaces).text
                dic['period'] = data
            except Exception, e:
                pass

            # try:
            #     data = xbrlFiling.find('edgar:assistantDirector', namespaces).text
            #     dic['assistantDirector'] = data
            # except Exception, e:
            #     pass
            #
            # try:
            #     data = xbrlFiling.find('edgar:assignedSic', namespaces).text
            #     dic['assignedSic'] = data
            # except Exception, e:
            #     pass
            #
            # try:
            #     data = xbrlFiling.find('edgar:fiscalYearEnd', namespaces).text
            #     dic['fiscalYearEnd'] = data
            # except Exception, e:
            #     pass

            # 获取文件 遍历files
            # xbrlFiles = xbrlFiling.find('edgar:xbrlFiles', namespaces)
            # for item in xbrlFiles.getchildren():
            #     try:
            #         itemDic = {}
            #         itemDic['fileName'] = item.attrib['{' + namespaces['edgar'] + '}' + 'file']
            #         itemDic['type'] = item.attrib['{' + namespaces['edgar'] + '}' + 'type']
            #         itemDic['size'] = item.attrib['{' + namespaces['edgar'] + '}' + 'size']
            #         itemDic['description'] = item.attrib['{' + namespaces['edgar'] + '}' + 'description']
            #         itemDic['url'] = item.attrib['{' + namespaces['edgar'] + '}' + 'url']
            #         files.append(itemDic)
            #     except Exception, e:
            #         print e
            #         pass

            dic['files'] = files
            LIST.append(dic)
            #			loadToDB(dic)
    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        #		consur.fail.insert({'path':path})
        print e

    num = len(LIST)
    # print num
    numFile.write('%d\n' % num)

    FILE = codecs.open(targetFile.replace('xbrl','%d_xbrl' % num), 'w+')
    try:
		FILE.write('%d\n' % num)
    except Exception, e:
        print e
    for item in LIST:
        print item
        FILE.write(item['cikNumber']+','+item['acceptanceDatetime']+','+item['period'])
        FILE.write('\n')


# def loadToDB(dic):
#     print '录入数据库。。。。'
#     try:
#         consur.test.insert(dic)
#     except Exception, e:
#         print '录入数据库失败'
#         consur.fail.insert({'path': dic['source']})
#         print e


if __name__ == '__main__':
    pool = Pool(5)

    def func(args, dire, files):
        for file in files:
            if file.endswith('.xml'):
                targetFile = os.path.join(os.path.expanduser('~'), 'Desktop', 'tongji', file.replace('.xml', '.txt'))
                pool.apply_async(praseXML, args=(os.path.join(dire, file), targetFile,))

    os.path.walk(__XML_PATH, func, ())
    pool.close()
    pool.join()








