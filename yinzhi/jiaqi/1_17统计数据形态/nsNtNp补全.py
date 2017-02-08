#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from collections import Counter
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

cpFindNs = re.compile(u'/ns\\b')
cpFindNt = re.compile(u'/nt\\b')
cpFindNposition = re.compile(u'/nposition\\b')
outFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'out.txt')
FILE = codecs.open(outFilePath, 'a', 'utf8')
nsDic = {}
ntDic = {}
npositionDic = {}
Divisions = []
SpliteStr =''

def loadFileToList(filePath):
    '''从文件路径 按行读取文件'''
    fileNameList = []
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            fileNameList.append(line)
    return fileNameList

def loadFile(filePath):
    '''从文件路径 按行读取文件'''
    relationDic = {}
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            splitedList = line.split("##")
            relationSet = set()
            sliceList = splitedList[3:]
            for idx in xrange(1, len(sliceList), 2):
                if sliceList[idx] > 0:
                    relationSet.add(splitedList[idx - 1])
            if len(relationSet):
                relationDic[splitedList[0]] = relationSet

    return relationDic

    #         fileNameList.append(line)
    # return fileNameList

def assembleSentence(npSentenceList):
    '''
    福建省/ns 漳州市/ns 东山县/ns 县长/nposition
    福建省/ns 东山县/ns 县委/nt 书记/nposition
    ____convertTo____
    [
    [县长/nposition, 东山县/ns, 漳州市/ns, 福建省/ns]
    [书记/nposition, 县委/nt, 东山县/ns, 福建省/ns]
    ]
    :param npSentence:
    :return:
    '''
    reverseList = []
    for item in npSentenceList:
        splitedList = item.split(" ")
        splitedList.reverse()
        reverseList.append(splitedList)
    return reverseList

def reverseOtherTree(sentenceList, idx, toCompleteList ,stack, findItem,  tag='nposition'):
    '''
    遍历查找其他数组元素
    :param sentenceList: sentence nposition树集合
    :param idx: 当前遍历下标idx
    :param findItem: 查找参照
    :return:
    '''

    stText = findItem.split("/")[0]
    returnList = []
    findSet = {
        'ns': lambda item: nsDic[item] if nsDic.has_key(item) else set(),
        'nt': lambda item: ntDic[item] if ntDic.has_key(item) else set(),
        'nposition': lambda item: npositionDic[item] if npositionDic.has_key(item) else set()
    }[tag](findItem)

    #若查找字典为空，略过 返回 [原数组]
    if not len(findSet):
        print findItem + u'**********未找到前驱'
        return None
    for innerIdx in xrange(idx, -1, -1):  # 倒序遍历 sentenceList[idx -1 ... 0]
        reverseList = sentenceList[innerIdx]
        # print innerIdx
        # print '_'.join(reverseList)
        for item in reverseList:#遍历一个 nposition树
            print u'遍历到', item
            itemText = item.split('/')[0]
            if item.endswith('nposition'):  # 若是nposition 则跳过
                continue
            else:#若不是nposition
                areaDivision = re.findall('%s$' % SpliteStr, itemText)
                if len(areaDivision) \
                        and areaDivision[0] in findSet \
                        and item != findItem\
                        and item not in stack\
                        and item not in returnList:
                        # and item not in toCompleteList:
                    # returnList.append(item)
                    print findItem + u'=========找到前驱：' + item
                    return item
                elif item in findSet \
                        and item != findItem\
                        and item not in stack\
                        and item not in returnList:
                        # and item not in toCompleteList:
                    print findItem + u'========找到前驱：' + item
                    return item
    print findItem + u'*******未找到前驱'
    return None
                    # returnList.append(item)

def completeSentence(sentenceList):
    for idx in xrange(len(sentenceList) - 1, -1, -1):#倒序遍历 sentenceList
        if idx == 0:#idx == 0 不做遍历
            continue
        _toCompleteList = sentenceList[idx]
        stack = []#空栈
        for innerIdx in xrange(len(_toCompleteList)):#将_toCompleteList元素入栈
            currentItem = _toCompleteList[innerIdx]#当前idx 元素
            if currentItem in stack:#若当前遍历元素在栈中，跳过此次循环
                continue
            if currentItem.endswith('/nposition'):
                stack.append(currentItem)
            flag = 1
            topItem = currentItem  # 最顶层元素
            tag = topItem.split('/')[-1]
            while flag:
                temp = reverseOtherTree(sentenceList, idx, _toCompleteList, stack, topItem, tag=tag)
                if temp != None:  # 长度为非0
                    tag = temp.split('/')[-1]
                    topItem = temp
                    if not currentItem.endswith('/nposition'):
                        stack.append(currentItem)
                    stack.append(temp)
                else:  # 没有顶层元素
                    flag = 0  # 跳出循环

            #计算_toCompleteList中有而 stack中没有的元素
        resultSet = set(_toCompleteList) - set(stack)
        for item in _toCompleteList:
            if item in resultSet:
                stack.append(item)
        # stack.reverse()
        # yield (idx, stack)

        print '========================='
        for item in sentenceList:
            print '__'.join(item)
        print '*************************'
        print '__'.join(_toCompleteList)
        print '__'.join(stack)
        print '========================='
        print '\n'
    # exit()

def main():
    inputFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'input.txt')

    #获取原始处理数据中的nposition分组
    with codecs.open(inputFilePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            splitedList = line.split("##")
            if len(splitedList) > 18:
                print splitedList[3]
                sentenceList = assembleSentence(splitedList[18:])
                # print '----------'
                # for item in sentenceList:
                #     print '__'.join(item)
                completeSentence(sentenceList)
            #     for idx, stack in completeSentence(sentenceList):
            #         # print ' '.join(sentenceList[idx])
            #         # print ' '.join(stack)
            #         sentenceList[idx] = stack
            #     # print '**********'
            #
            #     FILE.write('##'.join(splitedList[:18]))
            #     for item in sentenceList:
            #         item.reverse()
            #         FILE.write('##')
            #         FILE.write(' '.join(item))
            #     FILE.write('\r\n')
            # else:
            #     FILE.write(line + '\r\n')



if __name__ == "__main__":
    divisionFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'division.txt')
    Divisions.extend(loadFileToList(divisionFilePath))#读取区划
    SpliteStr = "(" + '|'.join(Divisions) + ")"
    # ns , nt, nposition关联统计数据路径
    nsCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'relationNsCount.txt')
    ntCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'relationNtCount.txt')
    nPositionCountFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'relationNpositionCount.txt')
    # 分别获取数据字典
    nsDic = loadFile(nsCountFilePath)
    ntDic = loadFile(ntCountFilePath)
    npositionDic = loadFile(nPositionCountFilePath)
    #
    # for item in ntDic[u'县委/nt']:
    #     print item
    # print '====='

    main()

