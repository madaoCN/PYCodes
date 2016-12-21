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
import json
import chardet

BASE_URL = 'https://gw.wmcloud.com/datamkt/whitelist/datapreview/%s?lang=zh'
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
    print url

    index = random.randint(0, len(IPANDPORT) - 1)
    proxy = {'http': 'http://%s' % IPANDPORT[index].strip()}
    print proxy
    try:
        prepare = Request('GET', url).prepare()
        r = session.send(prepare, proxies=proxy, timeout = 5)

        if len(r.content):
            resultJson = json.loads(r.content)
            title = resultJson['data']['title']
            print title
            desktopPath = os.path.join(dirPath, fileName)
            transfromPath = os.path.join(dirPath, title.replace(' ', '_').encode('utf8') + '##' + fileName)

            os.rename(desktopPath, transfromPath)

        # r = requests.get(url)
        # if not os.path.exists(dirPath):
        #     os.makedirs(dirPath)
        #     print '创建目录。。', dirPath
        desktopPath = os.path.join(dirPath, fileName)

        # if os.path.exists(desktopPath):
        #     print '文件名重复'
        #     desktopPath = desktopPath + '_1.csv'
        # if len(r.content):
        #     print '-------------' + desktopPath
        #     print  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        #     with open(desktopPath, "wb") as code:
        #         # code.write(MDCompressFile.gzip_compress(r.content))
        #         code.write(r.content)
    except Exception,e :
        print e, url
        print '出错了..'


if __name__ == "__main__":

    getTheRemoteAgent()
    dirPath = os.path.join(os.path.expanduser('~'), 'Desktop/通联CSV')

    pool = Pool(5)
    for item in os.listdir(dirPath):
        if item.endswith('.csv'):
            # print item
            ID = item.split('.csv')[0]
            if ID.isdigit():
                pool.apply_async(downUrlRetrieve, args=(dirPath, BASE_URL % ID, item))
    pool.close()
    pool.join()

