#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import MDRules
import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool,Process
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.instance
secCom = conn.secCom
baseStandard = conn.baseStandard
SupportItem = ['unit', 'context','schemaRef']

def praseXML(path):
    itemArr = []
    try:
        # namespaces = {'us-gaap': 'http://xbrl.us/us-gaap/2009-01-31'}
        # xmlDoc = ET.parse(path)
        # root = xmlDoc.getroot()
        from lxml import etree
        tree = etree.parse(path)
        root = tree.getroot()
        nsmap = root.nsmap
        #nsmap双向映射
        pamsn = {v:k for k,v in nsmap.items()}

        identifier = None
        soup = BeautifulSoup(codecs.open(path),'xml')
        try:
            identifier = soup.find('identifier').text
        except Exception, e:
            print e
            print '没有找到identifier'

        #获取当前文件名年数
        for child in root:
            # 去除辅助性元素
            if child.tag.split('}')[-1] in SupportItem:
                continue

            nameSpace = str(child.tag).strip('{').split('}')[0]

            #判断 tag前命名引用 是否是存在namespace中间的
            if pamsn[nameSpace] != None:
                #规则过滤
                attDic = child.attrib
                #拼接参数
                tag = child.tag
                text = child.text
                value = {}
                try:
                    value['CONTENTTEXT'] = text
                except Exception,e:
                    print e
                    print  'praseXML 57'
                #处理tag属性
                for attTemp in attDic:
                    try:
                        temp = attTemp.split('}')
                        # 判断属性中是否带有命名空间
                        if len(temp) > 1:
                            if pamsn[temp[0].strip('{')] != None:
                                value[pamsn[temp[0].strip('{')] + ':' + temp[-1]] = attDic[attTemp]
                        else:
                            value[attTemp] = attDic[attTemp]
                    except Exception, e:
                        print e
                        print 'praseXML 62'

                dic = {pamsn[nameSpace] +':'+ tag.split('}')[-1]:value}
                itemArr.append(dic)


        #根据fileName查找对象
        __name = os.path.basename(path)
        __year = '2008'

        try:
            row = secCom.xmltest.find_one({'files.fileName': __name})
            try:
                __year = row['period'][:4]
            except:
                print '查不到该条数据 设置为2008年'
        except Exception, e:
            print e
            print '查找失败!'

        pathPattern = path.split('Desktop')

        #原文件地址
        originPath = pathPattern[0] + 'Desktop/' + '10kOrgin' + pathPattern[1]
        #基本分类文档地址
        elementPath = pathPattern[0] + 'Desktop/' + '10kBase' + pathPattern[1]
        # 拓展分类文档地址
        instancePath = pathPattern[0] + 'Desktop/' + '10kExtend' + pathPattern[1]

        #写入原始文件
        writeToXML(nsmap, itemArr, originPath)
        originDic = {'filePath': path, 'tags': itemArr,
                     'fileName': os.path.basename(originPath),
                     'fileSize': os.path.getsize(originPath),
                     'identifier':identifier}

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(itemArr)
        loadToDB(originDic, 'origin')

        #写入元素
        element = []
        instance = []
        for item in itemArr:
            for key in item:
                try:
                    #首先匹配标准库表数据库
                    searchKey = key.split(':')[0]
                    row = baseStandard[__year].find_one({'prefix': searchKey})
                    if row:#和标准库匹配成功
                        element.append(item)
                    else:
                        # #匹配规则
                        if MDRules.matchBaseCategory(searchKey, nsmap):#如果是标准
                            element.append(item)
                        else:#否则是拓展的分类
                            instance.append(item)
                except Exception, e:
                    print e
                    print '查找失败!'

        writeToXML(nsmap, element, elementPath)
        elementDic = copy.deepcopy(originDic)
        elementDic['tags'] = element
        elementDic['filePath'] = elementPath
        elementDic['fileName'] = os.path.basename(elementPath)
        elementDic['fileSize'] = os.path.getsize(elementPath)
        loadToDB(elementDic, 'element')

        # 写入实例
        writeToXML(nsmap, instance, instancePath)
        instanceDic = copy.deepcopy(originDic)
        instanceDic['tags'] = instance
        instanceDic['filePath'] = instancePath
        instanceDic['fileName'] = os.path.basename(instancePath)
        instanceDic['fileSize'] = os.path.getsize(instancePath)
        loadToDB(instanceDic, 'instance')

    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e
        print consur.fails.insert({'failPath':path})
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


def writeToXML(nameSpace, itemArr, path):
    # 写入xml
    fileDir =  os.path.dirname(path)
    if not os.path.exists(fileDir):
        print '创建目录'
        print fileDir
        os.makedirs(fileDir)
    try:
        import MDCreateXML
        doc = MDCreateXML.initalXML(nameSpace, itemArr)
        MDCreateXML.writeXML(path, doc)
    except Exception, e:
        print e
        print '生成xml失败'

def loadToDB(dic, collectionName):
    '''
    写入数据库
    '''
    try:
        # 写入fileUrl地址
        col = consur[collectionName]
        col.insert(dic)
        print '录入数据库==============='
    except Exception, e:
        print e
        print '插入数据库失败==============='



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
    DIR = '/Users/lixiaorong/Desktop/test'
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


