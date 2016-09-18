#coding=utf8
import pymongo
import os
from bs4 import BeautifulSoup
import re
import codecs




if __name__ == "__main__":
    # getTheRemoteAgent()
    # getLinkAndArea(os.path.join(os.path.expanduser('/'), 'Volumes', 'TOSHIBA EXT', 'baike'))
    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.html') and file.startswith('answer') :#获取要删除的文件名
                name = file.lstrip('answer-').rstrip('.html')
                txtPath = os.path.join(dire, name+'.txt')
                xmlPath = os.path.join(dire, name+'.html')
                print txtPath
                print xmlPath
                os.remove(txtPath)
                os.remove(xmlPath)


    os.path.walk('/Users/liangxiansong/Desktop/财会分岗_data', funx, ())
    # getLinkAndArea('/Users/liangxiansong/Desktop/会计恒等式.txt')