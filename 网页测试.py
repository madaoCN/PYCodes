#coding=utf8
from multiprocessing import Process, Pool
import os, threading
import requests
from requests import Request, Session
import ssl
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
import urllib, random
import ConfigParser
import cookielib
import json
from ast import literal_eval
import chardet
from pymongo import MongoClient
import zlib

ssl._create_default_https_context = ssl._create_unverified_context



# 地址列表
IPANDPORT = []
# 获取代理列表
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

# 目标host
HOST_1 = 'http://clientapi.medical-lighter.com/user/short_userinfo'
HOST_2 = 'http://api.doctorpda.cn/api/comment/list?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&id=%s&p=1&limit=50&layer=TwoLayer&type=content'
HOST_3 = 'http://api.doctorpda.cn/api/app/client/open?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&loc=0&lon=0&lat=0&cur_channel=36e18idp80ct00e'
# session会话
session = Session()

#第一级url
def getUrl(target_url, index):
    # print target_url
    print index

    curentURL = target_url
    headers = {'User-Agent': '%E8%BD%BB%E7%9B%88%E5%8C%BB%E5%AD%A6/2.1.4 CFNetwork/758.3.15 Darwin/15.4.0',
               'Accept': '''*/*''',
                'Accept-Encoding': 'gzip, deflate',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept-Language': 'zh-cn',
    }

    s = r'''{\"device\":{\"platform\":\"android\",\"idfa\":\"e721e44d-ba72-3ec7-b90c-cd0d81bd8932\",\"macAddress\":\"9c:c1:72:6f:4d:59\",\"imei\":\"864036028378890\"},\"command\":\"message\\/notification\",\"user\":{\"uid\":\"302142\",\"nickname\":\"unicorn1369\",\"access_token\":\"y7NQT9BV8BB8F~nPdDjlf5ir7amkekGpjKpT7-QVn85sZ4FVertH-2w6EfgnPJIECwDGBGZbKqSAizFe\"},\"soft\":{\"coopId\":\"10020\",\"version\":\"2.1.4\",\"productId\":\"3001\"},\"request\":{\"user_id\":\"302142\"}}'''
    c = zlib.compress(s.encode('utf8'))

    byteStr = bytearray(c)
    for i in range(0, len(byteStr)):
        byteStr[i] = 0x5A ^ byteStr[i]

    prepare = Request('POST', curentURL, headers=headers, data= byteStr).prepare()
    print prepare.headers
    print prepare.body
    # print prepare._cookies
    # try多次
    attempts = 0
    success = False
    while attempts < 2 and not success:
        try:
            # ind = random.randint(0, len(IPANDPORT) - 1)
            # proxy = {'http': 'http://%s' % IPANDPORT[ind].strip()}
            # print proxy
            # result = session.send(prepare, timeout=20, proxies = proxy)
            result = session.send(prepare ,timeout=5)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts == 3:
                print '请求三次失败,跳过'
                return

    print "====================="
    print result.text

    arr = bytearray(result.text.encode('utf8'))
    for i in range(0, len(arr)):
        arr[i] = 0x5A ^ arr[i]

    print zlib.decompress(arr)

#解析用户名,关注,点赞,阅读数
def praseJsonForOne(response, index):
    print '+++++++++++++++++++++++++++++++++++++'
    client = MongoClient()
    myDB = client['zsyxDB']
    print myDB.web.insert({'index':index, 'data':response})


# if __name__ == '__name__':
getTheRemoteAgent()

pool = Pool(10)
for index in range(1):
    pool.apply_async(getUrl, args=(HOST_1, index))
pool.close()
pool.join()
print 'All subprocesses done.'




