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
    for matchInstance in matchArr:
        patternStr = r'[^a-zA-Z]*%s[^a-zA-Z]*' % matchInstance
        pattern = re.compile(patternStr)
        if re.search(pattern, nameSpace[searchKey]):#base备选
            if baseStandard.specialList.find_one({'prefix':searchKey, 'link':nameSpace[searchKey]}):
                return False#extend备选
            else:
                return True#base备选
    return False #extend备选


if __name__  == '__main__':
    print matchBaseCategory('gaap', {'gaap':'http://gaap.or.com'})
    string = '----201-415-16'
    result = re.search(r'[0-9]{4}', string)
    if result:
        print result.group(0)
