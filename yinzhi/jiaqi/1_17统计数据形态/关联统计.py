#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from collections import Counter

Divisions = []
SpliteStr = ''

cpCountNS = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?/ns(?!=\w)')
cpCountNT = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?\/nt(?!=\w)')
cpCountNPosition = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?\/nposition(?!=\w)')

cpFindNt = re.compile(u'/nt(?!=[\w])')#查找nt
cpFindNs = re.compile(u'/ns(?!=[\w])')#查找ns
cpFindArea = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?/ns(?!=\w)')

nsCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'relationNsCount.txt')
ntCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'relationNtCount.txt')
nPositionCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'relationNpositionCount.txt')

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

def findArea(originArea):
    '''
    寻找区划
    :param originArea:
    :return:
    '''
    result = re.findall(SpliteStr, originArea)
    for item in result:
        print originArea
        print item
    # print result

def countUpNPosition(splitedSTList):
    '''
    统计nposition前驱
    nposition 前驱数 前驱 前驱num
    '''
    # npositionSet = set()
    npositionDic = {}
    for item in splitedSTList:
        spliteByBlankList = item.split(' ')

        #判断最后一位是否是nposition
        # if not re.search('nposition', spliteByBlankList[-1]):
        #     print item
        npostionKey = spliteByBlankList[-1]

        if not npositionDic.has_key(npostionKey):#若没有键
            if len(spliteByBlankList) <= 1:  # 若无前驱
                npositionDic.update({npostionKey:[]})
            else:  #有前驱
                forItem = spliteByBlankList[-2]
                if cpFindNs.search(forItem):  # 若是ns
                    npositionDic[npostionKey] = re.findall(SpliteStr, forItem)
                else:  # 若是nt
                    npositionDic[npostionKey] = [forItem]
                # npositionDic.update({npostionKey: [forItem]})
        else: #若有键
            if len(spliteByBlankList) > 1:  # 有前驱
                forItem = spliteByBlankList[-2]

                if cpFindNs.search(forItem):  # 若是ns
                    list = npositionDic[npostionKey]
                    list.extend(re.findall(SpliteStr, forItem))
                    npositionDic[npostionKey] = list
                else:  # 若是nt
                    list = npositionDic[npostionKey]
                    list.append(forItem)
                    npositionDic[npostionKey] = list

    # for key, value in npositionDic.items():
    #     print key, Counter(value)
    for key, value in npositionDic.items():#遍历
        tempArr = [key]
        counterDic = Counter(value)
        tempArr.append(len(counterDic))
        for area in Divisions:
            tempArr.append(area)
            tempArr.append(counterDic[area] if counterDic[area] else '0')
        #遍历counterDic 中非Divisions 部分
        for item, itemValue in counterDic.items():
            if item not in Divisions:
                tempArr.append(item)
                tempArr.append(itemValue)

        nPositionCountFile.write('##'.join(map(lambda x:str(x) if isinstance(x, int) else x,tempArr)))
        nPositionCountFile.write('\r\n')

def countUpNt(splitedSTList):
    '''
    关联统计nt
    :param splitedSTList:
    :return:
    '''
    ntDic = {}
    for item in splitedSTList:
        if cpCountNT.findall(item):#若没有nt则过滤
            spliteByBlankList = item.split(' ')
            for idx in range(len(spliteByBlankList)):
                #遍历查找nt
                ntKey = spliteByBlankList[idx]
                if cpFindNt.search(ntKey):#若查找到nt
                    if not ntDic.has_key(ntKey):#未存在key
                        if idx > 0:#存在前驱
                            foreItem = spliteByBlankList[idx - 1]
                            if cpFindNs.search(foreItem):#若是ns
                                ntDic[ntKey] = re.findall(SpliteStr, foreItem)
                            else:#若是nt
                                ntDic[ntKey] = [spliteByBlankList[idx - 1]]
                    else:#存在key
                        if idx > 0:#存在前驱
                            foreItem = spliteByBlankList[idx - 1]
                            if cpFindNs.search(foreItem):  # 若是ns
                                findAreaResult = re.findall(SpliteStr, foreItem)
                                list = ntDic[ntKey]
                                list.extend(findAreaResult)
                                ntDic[ntKey] = list
                            else:  # 若是nt
                                list = ntDic[ntKey]
                                list.append(spliteByBlankList[idx - 1])
                                ntDic[ntKey] = list
    for key, value in ntDic.items():#遍历
        tempArr = [key]
        counterDic = Counter(value)
        tempArr.append(len(counterDic))
        for area in Divisions:
            tempArr.append(area)
            tempArr.append(counterDic[area] if counterDic[area] else '0')
        #遍历counterDic 中非Divisions 部分
        for item, itemValue in counterDic.items():
            if item not in Divisions:
                tempArr.append(item)
                tempArr.append(itemValue)

        ntCountFile.write('##'.join(map(lambda x:str(x) if isinstance(x, int) else x,tempArr)))
        ntCountFile.write('\r\n')



def countUpNs(splitedSTList):
    '''
    关联统计ns
    :param splitedSTList:
    :return:
    '''
    ntDic = {}
    for item in splitedSTList:
        if cpCountNS.findall(item):#若没有nt则过滤
            spliteByBlankList = item.split(' ')
            for idx in range(len(spliteByBlankList)):
                #遍历查找ns
                nsKey = spliteByBlankList[idx]
                if cpFindNs.search(nsKey):
                    if not ntDic.has_key(nsKey):#未存在key
                        if idx > 0:#存在前驱
                            foreItem = spliteByBlankList[idx - 1]
                            if cpFindNs.search(foreItem):#若是ns
                                ntDic[nsKey] = re.findall(SpliteStr, foreItem)
                            else:#若是nt
                                ntDic[nsKey] = [spliteByBlankList[idx - 1]]
                    else:#存在key
                        if idx > 0:#存在前驱
                            foreItem = spliteByBlankList[idx - 1]
                            if cpFindNs.search(foreItem):  # 若是ns
                                findAreaResult = re.findall(SpliteStr, foreItem)
                                list = ntDic[nsKey]
                                list.extend(findAreaResult)
                                ntDic[nsKey] = list
                            else:  # 若是nt
                                list = ntDic[nsKey]
                                list.append(foreItem)
                                ntDic[nsKey] = list
    for key, value in ntDic.items():#遍历
        tempArr = [key]
        counterDic = Counter(value)
        tempArr.append(len(counterDic))
        for area in Divisions:
            # tempArr.append(area if counterDic[area] else 'n/a')
            tempArr.append(area)
            tempArr.append(counterDic[area] if counterDic[area] else '0')
        #遍历counterDic 中非Divisions 部分
        for item, itemValue in counterDic.items():
            if item not in Divisions:
                tempArr.append(item)
                tempArr.append(itemValue)

        nsCountFile.write('##'.join(map(lambda x:str(x) if isinstance(x, int) else x,tempArr)))
        nsCountFile.write('\r\n')



if __name__ == "__main__":
    inputFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'input.txt')
    divisionFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'division.txt')
    Divisions.extend(loadFile(divisionFilePath))#读取区划
    SpliteStr = "(" + '|'.join(Divisions) + ")"

    splitedSTList = []
    with codecs.open(inputFilePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            list = line.split("##")
            if len(list) > 18:
                splitedSTList.append(list[18])

    countUpNPosition(splitedSTList)
    countUpNt(splitedSTList)
    countUpNs(splitedSTList)

