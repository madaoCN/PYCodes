#coding=utf8
import requests
from requests import Session, Request
from multiprocessing import Pool,Process
import time
import re
import os
import urllib
from bs4 import BeautifulSoup
import codecs
import pprint
BASE_URL = 'http://www.hotelaah.com/liren/'

def downUrlRetrieve(url):
    '''
    下载URL
    '''
    print "downloading with requests"
    try:
        # with codecs.open(url) as file:
        r = requests.get(BASE_URL + url)
        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find_all('table', {'border':'1'})
        secretaryTable = table[0]
        mayorTable = table[1]
        secretaryList = getNameDic(secretaryTable)
        mayorList = getNameDic(mayorTable)

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(secretaryList)
        # pp.pprint(mayorList)

        print '有%s任书记' % len(secretaryList)
        print '有%s任**长' % len(mayorList)
        return secretaryList, mayorList

    except Exception,e :
        print e
        print '出错了..'

def getNameDic(table):
    LIST = []
    trs = table.find_all('tr')
    for tr in trs:
        DIC = {}
        for td in tr.find_all('td'):
            result =' '.join(td.text.strip().split())
            if isinstance(result, str):
                pass
            if result != u'任期' and result != u'姓名' and result:
                if re.search('\d{4}', result):#是日期
                    arr = result.split('-')
                    DIC['forTime'] = arr[0].strip()
                    DIC['sufTime'] = arr[-1].strip()
                else:#不排除有"-至今"的情况
                    arr = result.split('-')
                    if len(arr) == 1:
                        DIC['name'] = arr
                    else:
                        DIC['forTime'] = arr[0].strip()
                        DIC['sufTime'] = arr[-1].strip()
        if len(DIC):
            LIST.append(DIC)
    return LIST



if __name__ == "__main__":
    sec, may = downUrlRetrieve('guizhou_anshun_xixiu.html')
    # pool = Pool(5)
    # pool.apply_async(downUrlRetrieve, args=(BASE_URL, ))
    # pool.close()
    # pool.join()

