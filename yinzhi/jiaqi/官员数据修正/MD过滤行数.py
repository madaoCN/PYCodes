#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from MDError import MDError
from MDNewFixModel import NewFixModel
import shutil

resultFile = os.path.join(os.path.expanduser("~"), "Desktop", 'hhhh.txt')

FILE = codecs.open(resultFile, 'a', 'utf8')
tagList = set()

def loadFile(filePath):
    fileNameSet = set()
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            resultList = line.split('##')
            stId = resultList[3]
            if stId in tagList:
                print stId
                FILE.write(line)
                FILE.write('\n')


if __name__ == "__main__":
    outFile = os.path.join(os.path.expanduser("~"), "Desktop", 'ids.txt')
    filePath = os.path.join(os.path.expanduser("~"), "Desktop", '166310.txt')
    with codecs.open(outFile, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            resultList = line.split('##')
            tagList.add(resultList[0] )
    print len(tagList)

    loadFile(filePath)

