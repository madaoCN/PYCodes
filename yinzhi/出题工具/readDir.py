#!/usr/bin/env python
#coding=utf8

import os
import codecs

def getDirs(dir, func, arg):
    os.path.walk(dir, func, arg)

def ls(arg, dirname, files):
    print dirname, 'has the files', files

# os.path.walk('/Users/lixiaorong/Desktop/test', ls, None)
#
# file = codecs.open('/Users/lixiaorong/Desktop/test/data.xlsx', encoding='utf8')
