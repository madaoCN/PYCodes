#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool

Divisions = []
SpliteStr = ''

cpCountNS = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?/ns\\b')
cpCountNT = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?\/nt\\b')
cpCountNPosition = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?\/nposition\\b')

cpFindArea = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?/ns\\b')

nsCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'nsCount.txt')
ntCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'ntCount.txt')
nPositionCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'npositionCount.txt')

nsCountFile = codecs.open(nsCountFilePath, 'a', 'utf8')
ntCountFile = codecs.open(ntCountFilePath, 'a', 'utf8')
nPositionCountFile = codecs.open(nPositionCountFilePath, 'a', 'utf8')

def loadFile(filePath):
    '''从文件路径 按行读取文件'''
    fileNameList = []
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            fileNameList.append(line)
    return fileNameList

def countUpNs(splitedSTList):
    '''
    统计ns
    原地名 地名 区划 是否有区划 出现频次
    '''
    nsDic = {}
    for outterItem in splitedSTList:
        list = cpCountNS.findall(outterItem)
        for item in list:
            originArea = item.strip('/ns')#原名称
            # tempArea = item.strip('/ns')
            # print item
            result = re.findall('%s$' % SpliteStr, originArea)

            if not len(result):#未属于区划范畴
                if nsDic.has_key(item):
                    itemList = nsDic[item]
                    num = itemList[4]
                    itemList[4] = str(int(num) + 1)
                    nsDic[item] = itemList
                else:
                    nsDic[item] = [originArea, originArea, "null", 'No', '1', outterItem]
            for thing in result:#有区划范畴
                #thing 区划
                if nsDic.has_key(item):
                    itemList = nsDic[item]
                    num = itemList[4]
                    itemList[4] = str(int(num) + 1)
                    nsDic[item] = itemList
                else:
                    # tempArea.replace(thing, '')
                    nsDic[item] = [originArea, originArea.replace(thing, ''), thing, 'Yes', '1']
                    # 遍历
    for key, value in nsDic.items():
        nsCountFile.write("##".join(value) + '\r\n')
        # nsCountFile.write('\n')

def countUpNt(splitedSTList):
    '''
    统计nt
    机构 出现频次
    '''
    ntDic = {}
    for item in splitedSTList:
        list = cpCountNT.findall(item)
        for item in list:
            item = item.strip('/nt')
            if ntDic.has_key(item):
                itemNum = ntDic[item]
                ntDic[item] = itemNum + 1
            else:
                ntDic[item] = 1
    #遍历
    for key, value in ntDic.items():
        ntCountFile.write(key + "##" + str(value) + '\r\n')
        # ntCountFile.write('\n')


def countUpNPosition(splitedSTList):
    '''
    统计nt
    机构 出现频次
    '''
    # npositionSet = set()
    npositionDic = {}
    for item in splitedSTList:
        list = cpCountNPosition.findall(item)
        for item in list:
            item = item.strip('/nposition')
            if npositionDic.has_key(item):
                itemNum = npositionDic[item]
                npositionDic[item] = itemNum + 1
            else:
                npositionDic[item] = 1
                # 遍历
    for key, value in npositionDic.items():
        nPositionCountFile.write(key + "##" + str(value) + '\r\n')
        # nPositionCountFile.write('\n')


if __name__ == "__main__":
    inputFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'input.txt')
    divisionFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'division.txt')
    Divisions.extend(loadFile(divisionFilePath))#读取区划
    SpliteStr = "(" + '|'.join(Divisions) + ")"
    print SpliteStr

    splitedSTList = []
    with codecs.open(inputFilePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            list = line.split("##")
            splitedSTList.append(list[6])

    #统计ns
    countUpNs(splitedSTList)
    countUpNt(splitedSTList)
    countUpNPosition(splitedSTList)
