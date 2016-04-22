#coding=utf8
from multiprocessing import Process, Pool
import os, threading
import requests
from requests import Request, Session
import ssl
from Crypto.Cipher import AES
import base64
import urllib
import ConfigParser
import cookielib
import json
from ast import literal_eval

class mycrypt():
    def __init__(self):
        self.key = 'doctorpda6666666'
        self.mode = AES.MODE_CBC
        self.IV = 'doctorpda6666666'

    def myencrypt(self,text):
        cryptor = AES.new(self.key,self.mode, self.IV)
        length = AES.block_size
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return self.ciphertext

    def mydecrypt(self,text):
        cryptor = AES.new(self.key,self.mode, self.IV)
        plain_text  = cryptor.decrypt(text)
        return plain_text

ssl._create_default_https_context = ssl._create_unverified_context

# 下一级的url列表
URLS = []
# 地址列表
IPANDPORT = []

# 目标host
HOST_1 = 'http://api.doctorpda.cn/api/v2/case/index?app_key=f1c18i2otirc0004&client_id=7c01ag7q3qcc0112&access_token=72ba7500-7562-40a0-a17e-f3cb465e3839&net=wifi&versionName=4.2.2&versionCode=85&source=app'
HOST_2 = 'http://api.doctorpda.cn/api/v2/case/comments?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&source=app'
HOST_3 = 'http://api.doctorpda.cn/api/app/client/open?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&loc=0&lon=0&lat=0&cur_channel=36e18idp80ct00e'
# session会话
session = Session()

# 获取代理列表
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

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
def getUrl(target_url, index, myCookie):
    # print target_url
    print index

    #拼接加密参数参数
    text = '''{"case_id":%s}''' % index
    en = mycrypt()
    entext = en.myencrypt(text)
    entext_base64 = base64.b64encode(entext)
    dataContent = urllib.quote(entext_base64)
    # print entext_base64
    if index != 0:
        data = {
            "data": entext_base64,
        }
    headers = {'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.2; Scale/2.00) doctorpda',
               'Accept': '''*/*''',
                'Accept-Encoding': 'gzip, deflate',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept-Language': 'zh-Hans-CN;q=1',
    }
    prepare = Request('POST', target_url, headers=headers, data=data, cookies=myCookie).prepare()
    print prepare.headers
    print prepare._cookies
    # print prepare.headers
    # print prepare.body
    # print prepare._cookies
    # try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            result = session.send(prepare, timeout=20)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts==3:
                print '请求三次失败,跳过'
                pass

    # print result.text
    # prase(result.text)
    # praseJsonForOne(result.text)
    # getNextUrl(target_url, index, prepare._cookies)

#解析用户名,关注,点赞,阅读数
def praseJsonForOne(response):
    try:
        result = json.loads(response)
    except Exception, e:
        print e
    data = result['data']
    #解密字符串
    en = mycrypt()
    detext_base64 = base64.b64decode(data)
    detext = en.mydecrypt(detext_base64).rstrip()
    print detext
    print "#######################################"
    try:
        jsonData = json.loads(detext.strip('\0'))
    except Exception, e:
        print e
    print jsonData
    if len(jsonData) == 0:
        return
    dataArr = []
    #用户名
    try:
        username = jsonData['caseTopic']['author']
        if username.strip() == '' or username is None:
            username = u'No'
    except Exception, e:
        username = u'No'
    dataArr.append(username)
    #关注数
    try:
        followNum = jsonData['caseTopic']['follow_count']
        if followNum is None:
            followNum = 0
    except Exception, e:
        followNum = 0
    dataArr.append(followNum)
    #点赞数
    try:
        likeNum = jsonData['caseTopic']['like_count']
        if likeNum is None:
            likeNum = 0
    except Exception, e:
        likeNum = 0
    dataArr.append(likeNum)
    # 阅读数
    try:
        readNum = jsonData['caseTopic']['read_count']
        if readNum is None:
            readNum = 0
    except Exception, e:
        readNum = 0
    dataArr.append(readNum)
    #评论数
    try:
        commentNum = jsonData['caseTopic']['comments']
        if commentNum is None:
            commentNum = 0
    except Exception, e:
        commentNum = 0
    dataArr.append(commentNum)
    # writeTofile(*dataArr)


def getNextUrl(target_url, index, myCookies):
    print '################################'
    print index
    headers = {
                'Host': 'api.doctorpda.cn',
               'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '''*/*''',
                'Connection': 'keep-alive',
                'Connection': 'keep-alive',
                # 'Cookie': 'JSESSIONID=D483F04DB2684B892A58D896130BA12A; Hm_lvt_bc9d4fa6469686fe63002104880688b1=1461150815; JSESSIONID=D483F04DB2684B892A58D896130BA12A; login_id=15221131593; secret_token=84bc894eada38d0b24fbcfd6163b914b',
                'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.2; Scale/2.00) doctorpda',
                'Accept-Language': 'zh-Hans-CN;q=1',
                'Accept-Encoding': 'gzip, deflate',
    }
    #拼接加密参数参数
    text = '''{"id":%s,"layer":"TwoLayer","type":"community_topic","p":1,"limit":10,"order":"like_count"}''' % index
    en = mycrypt()
    entext = en.myencrypt(text)
    entext_base64 = base64.b64encode(entext)
    dataContent = urllib.quote(entext_base64)

    if index != 0:
        data = {
            "data":dataContent
        }
    print data
    prepare = Request('POST', target_url, headers=headers, data=data, cookies=myCookies).prepare()
    print prepare._cookies
    print prepare.headers
    #try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            result = session.send(prepare, timeout=20)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts==3:
                print '请求三次失败,跳过'
                pass

    print result.text

#解析json
def praseJsonForTwo(response):
    result = json.loads(response)


def writeTofile(*arr):
    print '录入中...'
    path = os.path.expanduser(r'~/Desktop/data/data.txt')
    print path
    f = open(path, "a")
    print arr
    if arr:
        for rag in arr:
            if isinstance(rag, int):
                f.write(str(rag)+',')
            else:
                f.write(rag.encode('utf8')+',')
        f.write('\n')
        f.close()


# if __name__ == '__name__':
pool = Pool(10)
myCookie = getCookies()
for index in range(1):
    pool.apply_async(getNextUrl, args=(HOST_2, 12574, myCookie))
pool.close()
pool.join()
print 'All subprocesses done.'
