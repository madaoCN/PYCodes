#coding=utf8
from multiprocessing import Process, Pool
import os, threading
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random, selenium, re, json
import ssl
from Crypto.Cipher import AES
import base64
import urllib
import ConfigParser


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
HOST_2 = 'http://api.doctorpda.cn/api/v2/case/comments?app_key=f1c18i2otirc0004&client_id=7c01ag7q3qcc0112&access_token=72ba7500-7562-40a0-a17e-f3cb465e3839&net=wifi&versionName=4.2.2&versionCode=85&source=app '
HOST_3 = 'http://api.doctorpda.cn/api/app/client/open?app_key=f1c18i2otirc0004&client_id=7c01ag7q3qcc0112&access_token=72ba7500-7562-40a0-a17e-f3cb465e3839&net=wifi&versionName=4.2.2&versionCode=85&loc=0&lon=0&lat=0&cur_channel=36e18idp80ct00e1 '
# session会话
session = Session()

# 获取代理列表
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def getCookies():
    headers = {'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.3; Scale/2.00) doctorpda',
               'Accept-Encoding': 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept-Language': 'zh-Hans-CN;q=1',
               'Connection': 'keep - alive',
               'Accept': '*/*',
               }
    prepare = Request('GET', HOST_3, headers=headers).prepare()
    # try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            index = random.randint(0, len(IPANDPORT) - 1)
            proxy = {'http': 'http://%s' % IPANDPORT[index].strip()}
            print proxy
            result = session.send(prepare, timeout=20,)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts == 3:
                print '请求三次失败,跳过'
                pass

    myCookies = result.cookies
    print myCookies
    print result.text


#第一级url
def getUrl(target_url, index):
    print target_url
    print index

    #拼接加密参数参数
    text = '''{"case_id":%s}''' % index
    en = mycrypt()
    entext = en.myencrypt(text)
    entext_base64 = base64.b64encode(entext)
    dataContent = urllib.quote(entext_base64)
    if index != 0:
        data = {
            "data": dataContent,
            'source': 'app'
        }
    tempString = 'data=%s' % dataContent
    dataLen = len(tempString)

    headers = {'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.3; Scale/2.00) doctorpda',
               'Accept': '''*/*''',
                'Accept-Encoding': 'gzip, deflate',
               'Cookie': 'JSESSIONID=CE1D48E03C95B4D5D841F79AEE55B895; Hm_lvt_bc9d4fa6469686fe63002104880688b1=1460551175,1460717756; login_id=15221131593; secret_token=84bc894eada38d0b24fbcfd6163b914b; JSESSIONID=CE1D48E03C95B4D5D841F79AEE55B895;',
               'Connection': 'keep-alive',
               'Content - Type': 'application / x - www - form - urlencoded',
               'Accept - Language': 'zh - Hans - CN;q = 1',
                'Content - Length': dataLen,
    }
    prepare = Request('POST', target_url, headers=headers, data=data).prepare()
    # try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            result = session.send(prepare,timeout=20)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts==3:
                print '请求三次失败,跳过'
                pass

    print result.text
    print result.cookies
    # prase(result.text)
    # praseJsonForOne(result.text)



#解析用户名,关注,点赞,阅读数
def praseJsonForOne(response):
    result = json.loads(response)
    data = result['data']
    #解密字符串
    en = mycrypt()
    detext_base64 = base64.b64decode(data)
    detext = en.mydecrypt(detext_base64).rstrip()
    print detext

def getNextUrl(target_url, index):
    print index
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI P7-L09 Build/HuaweiP7-L09) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 doctorpda',
               'Accept-Encoding':'gzip',
               'Cookie':'JSESSIONID=CE1D48E03C95B4D5D841F79AEE55B895; Hm_lvt_bc9d4fa6469686fe63002104880688b1=1460551175,1460717756; JSESSIONID=CE1D48E03C95B4D5D841F79AEE55B895; login_id=15221131593; secret_token=84bc894eada38d0b24fbcfd6163b914b'
    }
    #拼接加密参数参数
    text = '''{"id":%s,"layer":"TwoLayer","type":"community_topic","p":1,"limit":10,"order":"like_count"}''' % index
    en = mycrypt()
    entext = en.myencrypt(text)
    entext_base64 = base64.b64encode(entext)
    dataContent = urllib.quote(entext_base64)

    if index != 0:
        data = {
            "data": dataContent
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

    print result.text
    # prase(result.text)
    # praseJsonForOne(result.text)


#解析json
def praseJson(response):
    result = json.loads(response)

    # print result
    #用户名
    try:
        username = result['username']
        if username.strip() == '' or username is None:
            username = u'no'
    except Exception, e:
        username = u'no'
    #真实姓名
    try:
        name = result['name']
        if name.strip() == '' or name is None:
            name = u'no'
    except Exception, e:
        name = u'no'
    #密码
    try:
        password = result['password'];
        if password.strip() == '' or password is None:
            password = u'no'
    except Exception, e:
        password = u'no'
    #生日
    try:
        birth = result['birth']
        if birth.strip() == '' or birth is None:
            birth = u'no'
    except Exception, e:
        birth = 'no'
    #医院/组织
    try:
        unit = result['unit']
        if unit.strip() == '' or unit is None:
            unit = u'no'
    except Exception, e:
        unit = u'no'
    #科室
    try:
        depart = result['depart']
        if depart.strip() == '' or depart is None:
            depart = u'no'
    except Exception, e:
        depart = u'no'
    # 职称
    try:
        title = result['title']
        if title.strip() == '' or title is None:
            title = u'no'
    except Exception, e:
        title = u'no'
    #职位
    try:
        occupation = result['occupation']
        if occupation.strip() == '' or occupation is None:
            occupation = u'no'
    except Exception, e:
        occupation = u'no'
    #粉丝数
    try:
        fanNum = result['fan_count']
        if fanNum is None:
            fanNum = 0
    except Exception, e:
        fanNum = 0
    #关注数
    try:
        followNum = result['follow_count']
        if followNum is None:
            followNum = 0
    except Exception, e:
        followNum = 0
    #电话
    try:
        phoneNum = result['mobile']
        if phoneNum.strip() == '' or phoneNum is None:
            phoneNum = u'no'
    except Exception, e:
        phoneNum = u'no'
    #教育水平
    try:
        education = result['education']
        if education.strip() == '' or education is None:
            education = u'no'
    except Exception, e:
        education = u'no'

    writeTofile(username, name, password, birth, unit, depart, title, occupation,
                 education, phoneNum, fanNum, followNum,)


def writeTofile(*arr):
    print '录入中...'
    path = os.path.expanduser(r'~/Desktop/test/test0-50000.txt')
    print path
    f = open(path, "a")
    print arr
    # if arr:
    #     for rag in arr:
    #         if isinstance(rag, int):
    #             f.write(str(rag)+',')
    #         else:
    #             f.write(rag.encode('utf8')+',')
    #     f.write('\n')
    #     f.close()


# if __name__ == '__name__':
getTheRemoteAgent()
pool = Pool(10)
# getCookies()
for index in range(1):
    pool.apply_async(getNextUrl, args=(HOST_2, 12509))
pool.close()
pool.join()
print 'All subprocesses done.'
