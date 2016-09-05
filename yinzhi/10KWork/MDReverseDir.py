#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import MDRules
import re
from multiprocessing import Pool,Process
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
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

        #xsd文件
        xsdPath = path[:-4]+'.xsd'
        xsdNsmap = None
        xsdPamsn = None
        if os.path.exists(xsdPath):
            xsdTree = etree.parse(xsdPath)
            xsdRoot = xsdTree.getroot()
            xsdNsmap = xsdRoot.nsmap
            xsdPamsn = {v: k for k, v in xsdNsmap.items()}

        #获取usgaap版本号
        __year = None
        try:
            findKey = None
            for key in nsmap:
                if key == None:
                    continue
                if re.search(u'us-gaap', key):
                    print key
                    findKey = key
            usgaap = nsmap[findKey]
            if usgaap:
               __year = usgaap.split('/')[-1].split('-')[0]
               print '获取到版本号' + __year + '========='
        except Exception, e:
            print e
            print '获取版本号失败=='

        #获取当前文件名年数
        for child in root:
            # 去除辅助性元素
            try:
                if child.tag.split('}')[-1] in SupportItem:
                    continue
            except Exception, e:
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
                        continue

                dic = {pamsn[nameSpace] +':'+ tag.split('}')[-1]:value}
                itemArr.append(dic)


        #根据fileName查找对象
        # __name = os.path.basename(path)
        # __year = '2008'

        # try:
        #     row = secCom.xmltest.find_one({'files.fileName': __name})
        #     try:
        #         __year = row['period'][:4]
        #     except:
        #         print '查不到该条数据 设置为2008年'
        # except Exception, e:
        #     print e
        #     print '查找失败!'

        pathPattern = path.split('home')
        #原文件地址
        originPath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')

        #基本分类文档地址(基本待定)
        basePath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')[:-4] + '_base' + pathPattern[1][-4:]
        # 基本分类文档地址(确认)
        baseSurePath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')[:-4] + '_baseSure' + pathPattern[1][-4:]
        # 基本分类文档地址(未确认)
        baseNotSurePath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')[:-4] + '_baseNotSure' + pathPattern[1][-4:]

        # 拓展分类文档地址(基本待定)
        extendPath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')[:-4] + '_ext' + pathPattern[1][-4:]
        # 拓展分类文档地址(确认)
        extendSurePath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')[:-4] + '_extSure' + pathPattern[1][-4:]
        # 拓展分类文档地址(未确认)
        extendNotSurePath = pathPattern[0] + 'home/' + '10kDeal/' + pathPattern[1].lstrip('/XBRLData')[:-4] + '_extNotSure' + pathPattern[1][-4:]
        #写入原始文件
        writeToXML(nsmap, itemArr, originPath)
        # originDic = {'filePath': path, 'tags': itemArr,
        #              'fileName': os.path.basename(originPath),
        #              'fileSize': os.path.getsize(originPath),
        #              'identifier':identifier}
        # loadToDB(originDic, 'origin')

        #写入元素
        base = []
        baseSure = []
        baseNotSure = []
        #拓展
        extend = []
        extendSure = []
        extendNotSure = []
        for item in itemArr:
            for key in item.keys():
                try:
                    if key == None:
                        continue
                    # #匹配规则
                    searchKey = key.split(':')[0]
                    if MDRules.matchBaseCategory(searchKey, nsmap): #如果是base备选
                        base.append(item)
                        row = baseStandard[__year].find_one({'name':key.split(':')[1]})
                        if row:  # 和标准库匹配成功 为base标准
                            baseSure.append(item)
                            # item['categoryTag'] = 'Base'
                        else:   #为拓展
                            extend.append(item)
                            # baseNotSure.append(item)
                            # item['categoryTag'] = 'noBase'
                    else:  # 否则是拓展备选
                        extend.append(item)
                        #判断是否是拓展和未确认
                        # if MDRules.matchExtCategory({searchKey:nsmap[searchKey]}, xsdNsmap):
                        #     extendSure.append(item)
                        # else:
                        #     extendNotSure.append(item)
                except Exception, e:
                    print e
                    print path
                    print '查找失败!'

        writeToXML(nsmap, base, basePath)
        # writeToXML(nsmap, baseSure, baseSurePath)
        # writeToXML(nsmap, baseNotSure, baseNotSurePath)
        # elementDic = copy.deepcopy(originDic)
        # elementDic['tags'] = base
        # elementDic['filePath'] = basePath
        # elementDic['fileName'] = os.path.basename(basePath)
        # elementDic['fileSize'] = os.path.getsize(basePath)
        # loadToDB(elementDic, 'base')


        # 写入实例
        writeToXML(nsmap, extend, extendPath)

        # writeToXML(nsmap, extendSure, extendSurePath)
        # writeToXML(nsmap, extendNotSure, extendNotSurePath)
        # instanceDic = copy.deepcopy(originDic)
        # instanceDic['tags'] = extend
        # instanceDic['filePath'] = extendPath
        # instanceDic['fileName'] = os.path.basename(extendPath)
        # instanceDic['fileSize'] = os.path.getsize(extendPath)
        # loadToDB(instanceDic, 'extend')

    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e
        print secCom.fails.insert({'failPath':path})
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
        col = secCom[collectionName]
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
    # DIR = '/Users/lixiaorong/Desktop/2016'
    DIR = os.path.join(os.path.expanduser("~"), 'Desktop/20140630#iMedicor')
    print DIR
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


