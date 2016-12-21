#coding=utf8
import requests
from requests import Session, Request
from multiprocessing import Pool,Process
import time
import re
import os
import urllib
import wget
import MDCompressFile
import random

BASE_URL = 'https://gw.wmcloud.com/datamkt/whitelist/downloadcsv/'
session = Session()

IPANDPORT = []
# 获取代理列表
def getTheRemoteAgent():
    listUrl = os.path.join(os.path.expanduser('~'), 'Desktop/proxy_list.txt')
    f = open(listUrl, "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def downUrlRetrieve(dirPath, url, fileName):
    '''
    下载URL
    '''
    localFilePath = os.path.join(dirPath, fileName)
    if os.path.exists(localFilePath):
        return

    index = random.randint(0, len(IPANDPORT) - 1)
    proxy = {'http': 'http://%s' % IPANDPORT[index].strip()}
    print proxy
    try:
        prepare = Request('GET', url).prepare()
        r = session.send(prepare, proxies=proxy)
        # r = requests.get(url)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
            print '创建目录。。', dirPath
        desktopPath = os.path.join(dirPath, fileName)

        # if os.path.exists(desktopPath):
        #     print '文件名重复'
        #     desktopPath = desktopPath + '_1.csv'
        if len(r.content):
            print '-------------' + desktopPath
            print  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
            with open(desktopPath, "wb") as code:
                # code.write(MDCompressFile.gzip_compress(r.content))
                code.write(r.content)
    except Exception,e :
        print e
        print '出错了..'


if __name__ == "__main__":

    getTheRemoteAgent()
    dirPath = os.path.join(os.path.expanduser('~'), 'Desktop/通联CSV')
    pool = Pool(5)
    for idx in range(0, 2000):
        print 'current id: ', idx
    #     downUrlRetrieve(dirPath, BASE_URL + str(idx) +'.csv', str(idx) + '.csv')
    #     time.sleep(2)
        pool.apply_async(downUrlRetrieve, args=(dirPath, BASE_URL + str(idx) +'.csv', str(idx) + '.csv'))
    pool.close()
    pool.join()

