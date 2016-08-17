#!/user/bin/env python
#coding=utf8
from bs4 import BeautifulSoup
import codecs
from xml.dom import minidom

def getTitle(file):
    try:
        print file
        file = codecs.open(file, encoding='utf8')
        soup = BeautifulSoup(file,'xml')
        tx = soup.TQuestion.Title.Text.text
        return tx
    except Exception, e:
        print 'error at dealWithXML-getTitle'
        print e
    return 'None'

def getVarible(file):
    List = []
    # try:
    #     file = codecs.open(file, encoding='utf8')
    #     soup = BeautifulSoup(file, 'lxml-xml')
    #     var = soup.Variables
    #     for tag in var.children:
    #         name = tag['name']
    #         tag['name'] = 'T1_'+name
    #         print tag
    # except Exception, e:
    #     print e
    #
    # return List
    try:
        doc = minidom.parse(file)
        root = doc.documentElement
        # var = root.getElementsByTagName("Variables")
        for c in root.getElementsByTagName('C'):
            List.append(c)
        for r in  root.getElementsByTagName('R'):
            List.append(r)
        return List
    except Exception, e:
        print 'error at getVarible+++++++++++++++'
        print e
        print 'error at getVarible---------------'
    return List
