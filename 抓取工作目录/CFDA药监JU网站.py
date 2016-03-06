# -*- coding: utf-8 -*-
from multiprocessing import Process, Pool
import os, threading
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random, selenium, re

# 下一级的url列表
URLS = []
# 地址列表
IPANDPORT = []
# 目标host
HOST = 'http://app1.sfda.gov.cn/datasearch/face3/'
# session会话
session = Session()

# 获取代理列表
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def getNextUrl(target_url, index):
    headers = {'User-Agent':'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
               'X-Requested-With':'XMLHttpRequest',
               "cache-control":"no-cache",
                "Content-Type":"application/x-www-form-urlencoded"
    }
    if index != 0:
        data = {
        'tableId':'33',
        'bcId':'118715801943244717582221630944',
        'tableName':'TABLE33',
        'viewtitleName':'COLUMN312',
        'viewsubTitleName':'COLUMN310',
        'curstart':'%s' % index,
        }
    else:
        data = {
        'tableId':'33',
        'bcId':'118715801943244717582221630944',
        'tableName':'TABLE33',
        'viewtitleName':'COLUMN312',
        'viewsubTitleName':'COLUMN310',
        }


    prepare = Request('POST', target_url, headers=headers, data=data).prepare()
    # try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            index = random.randint(0, len(IPANDPORT)-1)
            proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
            print proxy
            result = session.send(prepare, timeout=20, proxies=proxy)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts==3:
                print '请求三次失败,跳过'
                pass
    # print result.text
    prase(result.text)

def getNextPage(url):
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            index = random.randint(0, len(IPANDPORT)-1)
            proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
            print proxy
            result = session.get(url, timeout=20, proxies=proxy, headers={'User-Agent':'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',})
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts==3:
                print '请求三次失败,跳过'
                pass

    parseSecPage(result.text)

def parseSecPage(text):
    soup = BeautifulSoup(text, 'lxml')
    trs = soup.find_all('tr')
    args = []
    for tr in trs:
        td = tr.find('td', {'width':'83%'})
        if (td):
            print td.text
            args.append(td.text)
    writeTofile(*args)

def prase(text):
    soup = BeautifulSoup(text, 'lxml')
    As = soup.find_all('a')
    for a in As:
        urlSuff = a['href'].split('\'')[1]
        print HOST + urlSuff
        # 开启多线程获取下一级页面
        t = threading.Thread(target=getNextPage, args=(HOST + urlSuff,))
        # getNextPage(HOST+urlSuff)
        t.start()
        t.join()

def writeTofile(*arr):
    print arr
    path = os.path.expanduser(r'~/Desktop/data/test.txt')
    print path
    f = open(path, "a")
    if arr:
        for rag in arr:
            if isinstance(rag, int):
                f.write(str(rag)+',')
            else:
                f.write(rag.encode('utf8')+',')
        f.write('\n')
        f.close()


# if __name__ == '__name__':
getTheRemoteAgent()
pool = Pool()
for index in range(37):
    host = 'http://app1.sfda.gov.cn/datasearch/face3/search.jsp'
    pool.apply_async(getNextUrl, args=(host, index,))
pool.close()
pool.join()
print 'All subprocesses done.'
