#coding=utf8
import os
import GetDirFile
import lxml
from bs4 import BeautifulSoup
import pymongo
import codecs
from xml.etree import ElementTree
import chardet



__DOWNLOAD_BASE_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/downLoad/')
__XML_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/xmls/')
conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
consur = conn.secCom
collection = consur.xmlInfo



def praseXML(path):
    try:
        xmlDoc = ElementTree.parse(path)
        root = xmlDoc.getroot()
        #定义变量
        # title = link = guid = enclosure = description = pubDate = \
        # companyName = formType = filingDate = cikNumber = accessionNumber \
        # = fileNumber = acceptanceDatetime =  period = assistantDirector \
        # = assignedSic = fiscalYearEnd = xbrlFiles= 'N/A'

        index = 0
        lst_node = root.getiterator("item")


        for node in lst_node:
            dic = {}
            files = []
            dic['source'] = path.split('/')[-1]
            try:
                title = node.find('title').text
                dic['title'] = title
            except Exception, e:
                print 'title is None'

            try:
                link = node.find('link').text
                dic['link'] = link
            except Exception, e:
                print 'link is None'

            try:
                guid = node.find('guid').text
                dic['guid'] = guid
            except Exception, e:
                print 'guid is None'

            try:
                enclosure = node.find('enclosure').attrib['url']
                dic['enclosure'] = enclosure
            except Exception, e:
                print 'enclosure is None'

            try:
                description = node.find('description').text
                dic['description'] = description
            except Exception, e:
                print 'description is None'

            try:
                pubDate = node.find('pubDate').text
                dic['pubDate'] = pubDate
            except Exception, e:
                print 'pubDate is None'

            #属性
            namespaces = {'edgar': 'http://www.sec.gov/Archives/edgar'}  # add more as needed
            xbrlFiling = node.find('edgar:xbrlFiling', namespaces)
            try:
                data = xbrlFiling.find('edgar:companyName',namespaces).text
                dic['companyName'] = data
            except Exception, e:
                print 'companyName is None'

            try:
                data = xbrlFiling.find('edgar:formType',namespaces).text
                dic['formType'] = data
            except Exception, e:
                print 'formType is None'

            try:
                data = xbrlFiling.find('edgar:filingDate',namespaces).text
                dic['filingDate'] = data
            except Exception, e:
                print 'filingDate is None'

            try:
                data = xbrlFiling.find('edgar:cikNumber',namespaces).text
                dic['cikNumber'] = data
            except Exception, e:
                print 'cikNumber is None'

            try:
                data = xbrlFiling.find('edgar:accessionNumber',namespaces).text
                dic['accessionNumber'] = data
            except Exception, e:
                print 'accessionNumber is None'

            try:
                data = xbrlFiling.find('edgar:fileNumber',namespaces).text
                dic['fileNumber'] = data
            except Exception, e:
                print 'fileNumber is None'

            try:
                data = xbrlFiling.find('edgar:acceptanceDatetime',namespaces).text
                dic['acceptanceDatetime'] = data
            except Exception, e:
                print 'acceptanceDatetime is None'

            try:
                data = xbrlFiling.find('edgar:period',namespaces).text
                dic['period'] = data
            except Exception, e:
                print 'period is None'

            try:
                data = xbrlFiling.find('edgar:assistantDirector', namespaces).text
                dic['assistantDirector'] = data
            except Exception, e:
                print 'assistantDirector is None'

            try:
                data = xbrlFiling.find('edgar:assignedSic', namespaces).text
                dic['assignedSic'] = data
            except Exception, e:
                print 'assignedSic is None'

            try:
                data = xbrlFiling.find('edgar:fiscalYearEnd', namespaces).text
                dic['fiscalYearEnd'] = data
            except Exception, e:
                print 'fiscalYearEnd is None'

            #获取文件 遍历files
            xbrlFiles = xbrlFiling.find('edgar:xbrlFiles', namespaces)
            for item in xbrlFiles.getchildren():
                try:
                    itemDic = {}
                    itemDic['fileName'] = item.attrib['{'+namespaces['edgar']+'}'+'file']
                    itemDic['type'] = item.attrib['{' + namespaces['edgar'] + '}' + 'type']
                    itemDic['size'] = item.attrib['{' + namespaces['edgar'] + '}' + 'size']
                    itemDic['description'] = item.attrib['{' + namespaces['edgar'] + '}' + 'description']
                    itemDic['url'] = item.attrib['{' + namespaces['edgar'] + '}' + 'url']
                    files.append(itemDic)
                except Exception, e:
                    print e
                    print 'xbrlFile is None'

            dic['files'] = files
            loadToDB(dic)
    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        consur.fail.insert({'path':path})
        print e

    return dic

def loadToDB(dic):
    print '录入数据库。。。。'
    try:
        consur.xmltest.insert(dic)
    except Exception,e:
        print '录入数据库失败'
        consur.fail.insert({'path':dic['source']})
        print e

# if __name__ == '__main__':
#     dic =  praseXML('/Users/lixiaorong/Desktop/xmls/xbrlrss-2016-02.xml')
#     # loadToDB(dic)
#
# dic = praseXML('/Users/lixiaorong/Desktop/xmls/xbrlrss-2015-05.xml')










