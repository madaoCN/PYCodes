#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import MDRules
import re
from multiprocessing import Pool,Process
import MDCompressFile
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from lxml import etree
import pprint
import StringIO
import MDCreateXML

conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
secCom = conn.secCom
baseStandard = conn.baseStandard
SupportItem = ['unit', 'context','schemaRef']


def getVersionID(nsKey, pamsn):
    '''
    获取命名空间对应url中的版本号
    :param nsKey:
    :param pamsn:
    :return:
    '''
    try:
        if pamsn.has_key(nsKey):
            url = pamsn[nsKey]
            result = re.search('19|20\d{2}', url)
            if result:#获取到版本号
                version = result.group(0)
                return version
            else:
                return None
        else:
            return None
    except Exception, e:
        print e
        print '获取版本号失败'
        return None

def categoryXML(path,nsmap, itemArr):
    '''
    xml 规则匹配和分类
    :param path: 文件路径
    :param nsmap: 命名空间字典
    :param itemArr: xml 元素集合
    :return:
    '''
    currentDirName = os.path.dirname(path).split('/')[-1]  # 当前文件目录
    currentFileName = os.path.basename(path)  # 当前文件名
    targetDir = os.path.join(os.path.expanduser('~'), 'Desktop', 'XBRLWebDown', 'XBRLCate' ,currentDirName)
    # 原文件地址
    originPath = os.path.join(targetDir, currentFileName)
    # 基本分类文档地址(基本待定)
    basePath = os.path.join(targetDir, currentFileName.replace('.xml', '_base.xml'))
    # 基本分类文档地址(确认)
    baseSurePath = os.path.join(targetDir, currentFileName.replace('.xml', '_baseSure.xml'))
    # 基本分类文档地址(未确认)
    baseNotSurePath = os.path.join(targetDir, currentFileName.replace('.xml', '_baseNotSure.xml'))

    # 拓展分类文档地址(基本待定)
    extendPath = os.path.join(targetDir, currentFileName.replace('.xml', '_ext.xml'))
    # 拓展分类文档地址(确认)
    extendSurePath = os.path.join(targetDir, currentFileName.replace('.xml', '_extSure.xml'))
    # 拓展分类文档地址(未确认)
    extendNotSurePath = os.path.join(targetDir, currentFileName.replace('.xml', '_extNotSure.xml'))
    # 写入原始文件
    writeToXML(nsmap, itemArr, originPath)

    # 写入元素
    base = []
    baseSure = []
    baseNotSure = []
    # 拓展
    extend = []
    extendSure = []
    extendNotSure = []
    for item in itemArr:
        for key in item.keys():
            if key == None:
                continue
            # #匹配规则
            searchKey = key.split(':')[0]
            if MDRules.matchBaseCategory(searchKey, nsmap):  # 如果是base备选
                base.append(item)
                # __year = getVersionID(searchKey, nsmap)
                # if __year:
                #     # base.append(item)
                #     row = baseStandard[__year].find_one({'name': key.split(':')[1]})
                #     if row:  # 和标准库匹配成功 为base标准
                #         base.append(item)
                #         # item['categoryTag'] = 'Base'
                #     else:  # 标准库中无记录为拓展
                #         extend.append(item)
                #         # baseNotSure.append(item)
                #         # item['categoryTag'] = 'noBase'
                # else:  # 无版本号为拓展
                #     extend.append(item)
            else:  # 否则是拓展备选
                # 获取元素版本号
                extend.append(item)

                # 判断是否是拓展和未确认
                # if MDRules.matchExtCategory({searchKey:nsmap[searchKey]}, xsdNsmap):
                #     extendSure.append(item)
                # else:
                #     extendNotSure.append(item)

    print len(itemArr), len(base) , len(extend)

    # 写入基本分类文档
    writeToXML(nsmap, base, basePath)
    # writeToXML(nsmap, baseSure, baseSurePath)
    # writeToXML(nsmap, baseNotSure, baseNotSurePath)
    # elementDic = copy.deepcopy(originDic)
    # elementDic['tags'] = base
    # elementDic['filePath'] = basePath
    # elementDic['fileName'] = os.path.basename(basePath)
    # elementDic['fileSize'] = os.path.getsize(basePath)
    # loadToDB(elementDic, 'base')


    # 写入拓展分类文档
    writeToXML(nsmap, extend, extendPath)
    # writeToXML(nsmap, extendSure, extendSurePath)
    # writeToXML(nsmap, extendNotSure, extendNotSurePath)
    # instanceDic = copy.deepcopy(originDic)
    # instanceDic['tags'] = extend
    # instanceDic['filePath'] = extendPath
    # instanceDic['fileName'] = os.path.basename(extendPath)
    # instanceDic['fileSize'] = os.path.getsize(extendPath)
    # loadToDB(instanceDic, 'extend')

def praseXML(path):
    '''
    解析xml 获取命名空间, 和实例
    :param path:xml文档路径
    :return: 命名空间 和 实例集合
    '''
    itemArr = []#存储xml中实例
    try:
        tree = etree.parse(StringIO.StringIO(MDCompressFile.uncompress_file(path)), parser=etree.XMLParser(huge_tree=True))
        root = tree.getroot()
        nsmap = root.nsmap
        #nsmap双向映射
        pamsn = {v:k for k,v in nsmap.items()}

        #xsd文件获取命名空间, xsd获取命名空间 为了进一步确认是否是拓展或者未确认
        # xsdPath = path[:-4]+'.xsd'
        # xsdNsmap = None
        # xsdPamsn = None
        # if os.path.exists(xsdPath):
        #     xsdTree = etree.parse(xsdPath)
        #     xsdRoot = xsdTree.getroot()
        #     xsdNsmap = xsdRoot.nsmap
        #     xsdPamsn = {v: k for k, v in xsdNsmap.items()}


        #获取当前文件名年数
        for child in root:
            # 去除辅助性元素
            try:
                if child.tag.split('}')[-1] in SupportItem:
                    continue
            except Exception, e:
                continue

            nameSpaceLink = str(child.tag).strip('{').split('}')[0]

            #判断 tag前命名引用 是否是存在namespace中间的
            if pamsn[nameSpaceLink] != None:
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
                    print  'something wrong to get <CONTENTTEXT> ============'
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

                dic = {pamsn[nameSpaceLink] +':'+ tag.split('}')[-1]:value}
                itemArr.append(dic)
        return nsmap,itemArr
    except Exception, e:
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print e
        # print secCom.fails.insert({'failPath':path})
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'



def writeToXML(nameSpace, itemArr, path):
    '''
    将内容写入xml文档
    :param nameSpace:
    :param itemArr:
    :param path:
    :return:
    '''
    fileDir =  os.path.dirname(path)
    if not os.path.exists(fileDir):
        print '创建目录'
        print fileDir
        os.makedirs(fileDir)
    try:
        doc = MDCreateXML.initalXML(nameSpace, itemArr)
        MDCreateXML.writeXML(path, doc)
    except Exception, e:
        print e
        print '生成xml失败'
        print path

def loadToDB(dic, collectionName):
    '''
    录入数据库
    '''
    try:
        # 写入fileUrl地址
        col = secCom[collectionName]
        col.insert(dic)
        print '录入数据库==============='
    except Exception, e:
        print e
        print '插入数据库失败==============='

def main(path):
    '''
    函数入口
    :return:
    '''
    nsmap, itemArr = praseXML(path)
    categoryXML(path,nsmap, itemArr)

if __name__ == '__main__':
    # DIR = '/Users/lixiaorong/Desktop/2016'
    #两种工作模式 @1:目录递归
    DIR = os.path.join(os.path.expanduser("~"), 'Desktop', 'XBRLWebDown','XBRLDown')
    print DIR
    pool = Pool(5)
    def func(args,dire,files):
        for file in files:
            if file.endswith('.xml'):
               fileName = os.path.basename(file)
               splList = fileName.split('_')
               if len(splList) == 1:
                   targetPath = os.path.join(dire, file)
                   pool.apply_async(main, args=(targetPath,))
    
    os.path.walk(DIR, func, ())
    pool.close()
    pool.join()

    #@2:读路径列表
    # find . -type f -name "*-*[0-9].xml"
#    pool = Pool()
##    folderPath = os.path.join(os.path.expanduser("~"), 'Desktop', 'XBRLTestData','folder.txt')
#    folderPath = os.path.join(os.path.expanduser("/"), 'home', 'XBRL','folder.txt')
#    dirPath = folderPath.strip('/folder.txt')
#    idx = 0
#    with codecs.open(folderPath, 'r', encoding='utf8') as file:
#        for line in file.readlines():
#            fileName = os.path.basename(line).strip()
#            # if not re.search('_', fileName) and fileName.endswith('.xml'):
#            targetPath = os.path.join('/', dirPath, line.lstrip('./')).strip()
#            pool.apply_async(main, args=(targetPath,))
#    pool.close()
#    pool.join()
#    print 'processed ============'


