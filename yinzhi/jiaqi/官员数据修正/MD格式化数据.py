#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from MDError import MDError
from MDNewFixModel import NewFixModel

def loadFile(filePath):
    '''从文件路径 按行读取文件'''
    fileNameList = []
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            fileNameList.append(line)
    return fileNameList


def putInitalSentence(idTag, model):
    '''model 中放置原始句子'''

def main():
    splitTagDir= os.path.join(os.path.expanduser('~'), 'Desktop', 'splitTag')
    splitSentenceDir= os.path.join(os.path.expanduser('~'), 'Desktop', 'splitSentence')
    targetFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', 'target.txt')
    FILE =  codecs.open(os.path.join(os.path.expanduser('~'), 'Desktop','out.txt'), 'a', 'utf8')
    idTagDic = {}# key filename value [sentenceId,...]
    resultDic = {}
    with codecs.open(targetFilePath, 'r', 'utf16') as file:
        for line in file.readlines():
            line = line.strip()
            list = line.split('\t')
            model = NewFixModel()
            model.id = list[0]
            model.sentenceId = list[1]
            model.hmName = list[2]
            model.hmId = list[3]
            model.fileName = list[4]
            # print model.fileName
            resultDic.update({model.sentenceId:model})
            if idTagDic.has_key(model.fileName):# 若存在key 添加进value字典
                list = idTagDic.get(model.fileName)
                list.append(model.sentenceId)
                idTagDic[model.fileName] = list
            else:
                idTagDic[model.fileName] = [model.sentenceId]
    for fileName, idTagList in idTagDic.items():
        splitSentenceList = loadFile(os.path.join(splitSentenceDir, fileName))
        splitTagList = loadFile(os.path.join(splitTagDir, fileName))
        for idx in range(len(idTagList)):#遍历原始句子数组
            originSentence = splitSentenceList[idx]
            originTag = splitTagList[idx]
            #model赋值
            model = resultDic[idTagList[idx]]
            model.originSentence = originSentence
            model.splitedSentence = originTag
            FILE.write(model.values())
            FILE.write('\n')


if __name__ == "__main__":
    main()