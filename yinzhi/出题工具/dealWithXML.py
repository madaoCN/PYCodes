#!/user/bin/env python
#coding=utf8
from bs4 import BeautifulSoup
import codecs
from xml.dom import minidom

FILE = '/Users/lixiaorong/Desktop/编制转账支票_支付原材料价款（供应方，金额，口令）.xml'

def getTitle(file):
    try:
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
    doc = minidom.parse(file)
    root = doc.documentElement
    # var = root.getElementsByTagName("Variables")
    for c in root.getElementsByTagName('C'):
        List.append(c)
    for r in  root.getElementsByTagName('R'):
        List.append(r)
    return List
