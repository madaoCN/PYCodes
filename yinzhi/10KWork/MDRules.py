#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import re

conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
baseStandard = conn.baseStandard
matchArr = ['xbrl', 'gaap', 'wc', 'w3c', 'sec', 'fasb']

def matchBaseCategory(searchKey, nameSpace):
    '''
    :return: 是否是基本分类文档
    '''
    for matchInstance in matchArr:
        if matchInstance == None:
            continue
        patternStr = r'[^\/a-zA-Z]+%s[^\/a-zA-Z]+' % matchInstance
        pattern = re.compile(patternStr)
        if re.search(pattern, nameSpace[searchKey]):#base备选
            # print searchKey, re.search(pattern, nameSpace[searchKey]).group(0)
            if baseStandard.specialList.find_one({'prefix':searchKey, 'link':nameSpace[searchKey]}):
                return False#extend备选
            else:
                return True#base备选
    return False #extend备选

def matchExtCategory(searchDic, extSpace):
    '''
    判断是否是拓展模式文档
    '''
    for searchKey in searchDic.keys():
        if not extSpace[searchDic]:#拓展中没有
            return False
        if extSpace[searchKey] == searchDic[searchKey]:#拓展中有
            return True
    return False


if __name__  == '__main__':
    print matchExtCategory({'gaap':'http://gaap.orfdsf.com'}, {'gaap':'http://gaap.or.com'})

