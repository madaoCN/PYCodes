#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import copy
import codecs
import re

conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
baseStandard = conn.baseStandard
matchArr = ['xbrl', 'gaap', 'wc', 'w3c', 'sec', 'fasb']

def matchBaseCategory(searchKey, nameSpace):
    '''
    :return: 是否是基本分类文档
    '''
    link = None
    if not nameSpace.has_key(searchKey):
        return False
    link = nameSpace[searchKey]
    for matchInstance in matchArr:
#        patternStr = r'[^\.\/a-zA-Z]*%s[^\. \/a-zA-Z]*' % matchInstance
        patternStr = '[^a-zA-Z]%s[^a-zA-Z]' % matchInstance
        if re.search(patternStr, link):#base备选
            # print searchKey, re.search(pattern, nameSpace[searchKey]).group(0)
            if baseStandard.specialList.find_one({'prefix':searchKey, 'link':nameSpace[searchKey]}):
                return False#extend备选
            else:
                return True
                
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

