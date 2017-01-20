#coding= utf8

import codecs
import os
import re
from multiprocessing import Pool
import pandas as pd
from bs4 import BeautifulSoup
import xml.dom.minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def sortNposition(list):
    '''
    分割ns， nt，
    :param list:
    :return:
    '''

if __name__ == "__main__":

    u = u'汉'
    print repr(u)  # u'\u6c49'
    s = u.encode('UTF-8')
    print repr(s)  # '\xe6\xb1\x89'
    u2 = s.decode('UTF-8')
    print repr(u2)  # u'\u6c49'

    s1 = '哈'
    print repr(s1)

    # excel = pd.read_html('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls')
    # print excel

    # import codecs
    # from bs4 import BeautifulSoup
    #
    # with codecs.open('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls', 'r') as file:
    #     soup = BeautifulSoup(file, 'lxml')
    #     print soup
        # for item in soup.find_all('worksheet'):
        #     ''''sheet0-------...'''
        #     for innerItem in item.find_all('cell'):
        #         print innerItem.text

    # dom = xml.dom.minidom.parse('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls')
    # root = dom.documentElement
    # # print dir(root)
    # for node in dom.getElementsByTagName('worksheet'):
    #     print node

    # ET.register_namespace('xmlns', 'schemas-microsoft-com:office:spreadsheet')
    # ET.register_namespace('html', 'http://www.w3.org/TR/REC-html40')
    # ET.register_namespace('o', 'schemas-microsoft-com:office:office')
    # tree = ET.parse('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls')







