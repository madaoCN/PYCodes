#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from MDError import MDError
from MDNewFixModel import NewFixModel
import shutil

def fliterFiles(dirPath, outDir,fileNameList):
    '''通过文件名列表过滤文件'''
    for item in fileNameList:
        filePath = os.path.join(dirPath, item)
        targetPath = os.path.join(outDir, item)
        if os.path.exists(filePath):#如果文件存在 则拷贝至out文件夹
            shutil.copyfile(filePath, targetPath)
        else:
            print '文件不存在'
            print item

def loadFile(filePath):
    fileNameSet = set()
    with codecs.open(filePath, 'r', 'utf16') as file:
        for line in file.readlines():
            line = line.strip()
            splitedList = line.split("\t")
            idItem = splitedList[0] #id
            hmName = splitedList[2] #人名
            hmId = splitedList[3] #人名IDfileNameList
            fileName = splitedList[4] #文件名
            fileNameSet.add(fileName)
    return list(fileNameSet)

if __name__ == "__main__":
    outDir = os.path.join(os.path.expanduser("~"), "Desktop", 'out')
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    filePath = os.path.join(os.path.expanduser("~"), "Desktop", 'target.txt')
    dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'target')
    fileNameList = loadFile(filePath)
    print len(fileNameList)
    fliterFiles(dirPath=dirPath, outDir = outDir,fileNameList=fileNameList)
