#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random

IPANDPORT = []
TARGET_HOST = 'http://fz.58.com/job/pn%s/?key=ios&cmcskey=ios&final=1&specialtype=gls'
session = Session()

# 获取代理列表
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def run_pro(target_url):
    index = random.randint(0, len(IPANDPORT)-1)
    proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'X-Requested-With':'XMLHttpRequest',
               "cache-control":"no-cache",
                "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {}
    print proxy

    prepare = Request('GET', target_url).prepare()
    try:
        result = session.send(prepare, proxies=proxy)
    except Exception, e:
        print '请求失败'
        print e
    print result.text
    # prase(result.text)


def prase(text):
    soup = BeautifulSoup(text, 'lxml')
    div = soup.find('div', {'id':'infolist'})
    dls = div.find_all('dl')

    for dl in dls:
        text = []
        index = 0
        for a in dl.find_all('a'):
            if index != 2:
                text.append(a.string.decode('utf8'))
            index += 1
            print a.string
        text.append(dl.find('dd', {'class':'w96'}).string.decode('utf8'))
        print dl.find('dd', {'class':'w96'}).string.decode('utf8')
        writeTofile(text)

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
print IPANDPORT
pool = Pool()
for index in range(1):
    host = 'http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=33&tableName=TABLE33&title=互联网药品交易服务&bcId=118715801943244717582221630944'
    pool.apply_async(run_pro, args=(host,))
pool.close()
pool.join()
print 'All subprocesses done.'
