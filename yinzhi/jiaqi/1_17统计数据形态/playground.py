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


    # excel = pd.read_html('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls')
    # print excel

    # import codecs
    # from bs4 import BeautifulSoup
    #
    FILe = codecs.open('/Users/liangxiansong/Desktop/out.txt', 'a')
    with codecs.open('/Users/liangxiansong/Desktop/test.txt', 'r') as file:
        for item in file.readlines():
            result = item.strip('\r\n')
            if len(result) > 0:
                FILe.write(result)
                FILe.write('\n')

    # dom = xml.dom.minidom.parse('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls')
    # root = dom.documentElement
    # # print dir(root)
    # for node in dom.getElementsByTagName('worksheet'):
    #     print node

    # ET.register_namespace('xmlns', 'schemas-microsoft-com:office:spreadsheet')
    # ET.register_namespace('html', 'http://www.w3.org/TR/REC-html40')
    # ET.register_namespace('o', 'schemas-microsoft-com:office:office')
    # tree = ET.parse('/Users/liangxiansong/Desktop/投资者互动000004.SZ.xls')







