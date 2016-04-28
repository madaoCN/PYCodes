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

ssl._create_default_https_context = ssl._create_unverified_context



# 地址列表
IPANDPORT = []
COOKIES = requests.cookies.RequestsCookieJar()
# 目标host
HOST_1 = 'http://api.doctorpda.cn/c/%s?app_key=f1c18i2otirc0004&client_id=7c01ag7q3qcc0112&access_token=72ba7500-7562-40a0-a17e-f3cb465e3839&net=wifi&versionName=4.2.2&versionCode=85'
HOST_2 = 'http://api.doctorpda.cn/api/comment/list?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&id=%s&p=1&limit=50&layer=TwoLayer&type=content'
HOST_3 = 'http://api.doctorpda.cn/api/app/client/open?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&loc=0&lon=0&lat=0&cur_channel=36e18idp80ct00e'
# session会话
session = Session()

def getCookies():
    headers = {'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.2; Scale/2.00) doctorpda',
               'Accept-Encoding': 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept-Language': 'zh-Hans-CN;q=1',
               'Connection': 'keep - alive',
               'Cookies':'login_id=15221131593',
               'Accept': '*/*',
               }
    prepare = Request('GET', HOST_3, headers=headers).prepare()
    # try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            result = session.send(prepare, timeout=20,)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts == 3:
                print '请求三次失败,跳过'
                pass

    # print result.text
    print result.cookies
    return result.cookies

#第一级url
def getUrl(target_url, index):
    # print target_url
    print index

    curentURL = target_url % index
    headers = {'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.2; Scale/2.00) doctorpda',
               'Accept': '''*/*''',
                'Accept-Encoding': 'gzip, deflate',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept-Language': 'zh-Hans-CN;q=1',
    }
    prepare = Request('GET', curentURL, cookies=COOKIES).prepare()
    # print prepare.headers
    # print prepare.body
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
    praseJsonForOne(result.text, index)

#解析用户名,关注,点赞,阅读数
def praseJsonForOne(response, index):
    print '+++++++++++++++++++++++++++++++++++++'
    client = MongoClient()
    myDB = client['zsyxDB']
    print myDB.web.insert({'index':index, 'data':response})


# if __name__ == '__name__':
myCookie = getCookies()

# pool = Pool(10)
# for index in range(20000,30000):
#     pool.apply_async(getUrl, args=(HOST_1, index))
# pool.close()
# pool.join()
# print 'All subprocesses done.'
client = MongoClient()
myDB = client['zsyxDB']
print myDB.web.insert({'index':index, 'data':response})



