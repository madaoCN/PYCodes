#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ConfigParser import ConfigParser
import sys, os
import random

# 获取代理列表
def getRandomRemoteAgent():
    cf = ConfigParser()
    cf.read('config.ini')
    fileName = cf.get('userAgent', 'file_Name')
    desktopPath = os.path.join(os.path.expanduser("~"), 'Desktop')
    f = open(desktopPath + '/' +fileName, "r")
    #获取文件行数
    fileLines = getFileLineNum(f)
    ranNum = random.randint(0, fileLines)
    #读取文件指定行
    index = 0
    f = open(desktopPath + '/' + fileName, "r")
    for line in f:
        if index == ranNum:
            f.close()
            return line
        index += 1


def getFileLineNum(file):
    '''
    获取文件行数
    '''
    count = 0
    while True:
        buffer = file.read(1024 * 8192)
        if not buffer:
            break
        count += buffer.count('\n')
    return count

print getRandomRemoteAgent()