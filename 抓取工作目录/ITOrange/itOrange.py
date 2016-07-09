#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random
import pymongo
import re

IPANDPORT = []
TARGET_HOST = 'http://www.itjuzi.com/company?scope=47'
session = Session()
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)

# 获取代理列表
def getTheRemoteAgent():
    f = open("/Users/liangxiansong/Desktop/proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def run_pro(target_url, page):
    #construct page
    realUrl = target_url
    if page != 1:
        realUrl = target_url + '&page=%s' % (page, )

    print realUrl
    index = random.randint(0, len(IPANDPORT)-1)
    proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
               "cache-control":"no-cache",
               "Content-Type":"application/x-www-form-urlencoded",
               'Host': 'www.itjuzi.com',
               'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8Accept - Encoding:gzip, deflate, sdch',
               'Accept - Language': 'zh - CN, zh;q = 0.8'
    }
    data = {}
    print proxy

    prepare = Request('GET', realUrl, headers=headers).prepare()
    try:
        # result = session.send(prepare, proxies=proxy)
        result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        return
    print 'prasing.......'
    prase(result.text)

def prase(text):
    '''
    '''
    soup = BeautifulSoup(text, 'lxml')
    div = soup.find_all('div', {'class':'sec'})
    aTags = div[2].find_all('a')
    prog = re.compile(r"http://www.itjuzi.com/company/")
    URLS = set()
    for a in aTags:
        if prog.match(a['href']):
            url = a['href']
            URLS.add(url)

    for url in URLS:
        print url
        db = conn.itJuZi
        collections = db.URLS
        collections.insert({'url':url})
    print 'load to db.....'

    # for dl in dls:
    #     text = []
    #     index = 0
    #     for a in dl.find_all('a'):
    #         if index != 2:
    #             text.append(a.string.decode('utf8'))
    #         index += 1
    #         print a.string
    #     text.append(dl.find('dd', {'class':'w96'}).string.decode('utf8'))
    #     print dl.find('dd', {'class':'w96'}).string.decode('utf8')
    #     writeTofile(text)

def writeTofile(*arr):
    print arr
    path = os.path.expanduser(r'~/Desktop/data/test.txt' % (officeTemp))
    print path
    f = open(path, "a")
    if arr:
        for rag in arr:
            if isinstance(rag, int):
                f.write(str(rag)+',')
            else:
                f.write(rag.encode('UTF-8')+',')
        f.write('\n')
        f.close()


# if __name__ == '__name__':
getTheRemoteAgent()
# print IPANDPORT
pool = Pool(3)
for index in range(24, 26):
    pool.apply_async(run_pro, args=(TARGET_HOST, index))
pool.close()
pool.join()
conn.close()


print 'All subprocesses done.'
