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
    praseJsonForOne(result.text, index, myCookie)
    # getNextUrl(target_url, index, prepare._cookies)

#解析用户名,关注,点赞,阅读数
def praseJsonForOne(response, index, myCookies):
    print '################################praseJsonForOne'
    try:
        result = json.loads(response)
    except Exception, e:
        print e
    data = result['data']
    #解密字符串
    en = mycrypt()
    detext_base64 = base64.b64decode(data)
    detext = en.mydecrypt(detext_base64).rstrip()
    # print "#######################################"
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
            username = u'N/A'
    except Exception, e:
        username = u'N/A'
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
    # writeTofile(*dataArr)

    getNextUrl(index, myCookies, dataArr)


def getNextUrl(index, myCookies, dataArr):
    print '################################getNextUrl'
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
    text = '''{"id":%s,"layer":"TwoLayer","type":"community_topic","p":1,"limit":50,"order":"like_count"}''' % index
    en = mycrypt()
    entext = en.myencrypt(text)
    entext_base64 = base64.b64encode(entext)
    dataContent = urllib.quote(entext_base64)

    if index != 0:
        data = {
            "data":entext_base64
        }
    print data
    prepare = Request('POST', HOST_2, headers=headers, data=data, cookies=myCookies).prepare()
    # print prepare._cookies
    # print prepare.headers
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

    praseJsonForTwo(result.text, dataArr)

#解析json
def praseJsonForTwo(response, dataArr):
    print '################################praseJsonForTwo'
    try:
        result = json.loads(response)
    except Exception, e:
        print e
    data = result['data']
    # 解密字符串
    en = mycrypt()
    detext_base64 = base64.b64decode(data)
    detext = en.mydecrypt(detext_base64).rstrip()
    print detext
    # print "#######################################"
    try:
        jsonData = json.loads(detext.strip('\0'))
    except Exception, e:
        print e
    #解析字符串
    #评论数
    try:
        commentNum = jsonData['totalRow']
        dataArr.append(commentNum)
        if readNum is None:
            commentNum = 0
    except Exception, e:
        commentNum = 0
    #评论用户统计

    myDic = {}
    try:
        comments = jsonData['list']
        # 没有用户评论
        if comments is None or len(comments) <=0:
            myDic['N/A'] = 0
        else:
        #有用户评论,那么开始遍历
            for comment in comments:
                try:
                    tempName = comment['username']
                    if tempName is None:
                        tempName = 'N/A'
                    else:
                        #若果已经有该用户名
                        if myDic.has_key(tempName):
                            count = myDic[tempName]
                            myDic[tempName] = count + 1
                        #如果没有该用户名
                        else:
                            myDic[tempName] = 1
                except Exception, e:
                    print e
                    tempName = 'N/A'
                    myDic[tempName] = 0
                #遍历子评论
                finally:
                    try:
                        childs = comment['children']
                        # 没有子评论
                        if childs is None or len(childs) <= 0:
                            print '没有子评论'
                        else:
                            # 有用户子评论,那么开始遍历
                            for child in childs:
                                try:
                                    childUser = child['username']
                                    if childUser is None:
                                        childUser = 'N/A'
                                    else:
                                        # 若果已经有该用户名
                                        if myDic.has_key(childUser):
                                            count = myDic[childUser]
                                            myDic[childUser] = count + 1
                                        # 如果没有该用户名
                                        else:
                                            myDic[childUser] = 1
                                except Exception, e:
                                    print e
                    except Exception, e:
                        print e
    except Exception, e:
        print e
        myDic['N/A'] = 0

    writeTofile(dataArr, myDic)




def writeTofile(dataArr, myDic):
    print '##########################writeTofile'
    print dataArr
    print myDic
    print '录入中...'

    path = os.path.expanduser(r'~/Desktop/data/data.txt')
    print path
    f = open(path, "a")
    if dataArr:
        for rag in dataArr:
            if isinstance(rag, int):
                f.write(str(rag)+',')
            else:
                f.write(rag.encode('utf8')+',')
    if myDic:
        for key in myDic:
            print key
            write_str = key.encode('utf8') + ':' + str(myDic[key]) + ','
            f.write(write_str)

    f.write('\n')
    f.close()


# if __name__ == '__name__':
pool = Pool(10)
myCookie = getCookies()
for index in range(1):
    pool.apply_async(getUrl, args=(HOST_1, 12522, myCookie))
pool.close()
pool.join()
print 'All subprocesses done.'
