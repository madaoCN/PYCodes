# -*- coding: utf-8 -*-
from multiprocessing import Process, Pool
import os, threading
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random, selenium, re, json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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
    f = open("proxy_list2.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def getNextUrl(target_url, index):
    print index
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI P7-L09 Build/HuaweiP7-L09) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 doctorpda',
               'Accept-Encoding':'gzip'
    }
    if index != 0:
        data = {
        'jsessionid':'C154F3823E372E2A3D9D0AD40B74A21B',
        'postId':'%s' % index,
        }
    # else:
    #     data = {
    #     'tableId':'33',
    #     'bcId':'118715801943244717582221630944',
    #     'tableName':'TABLE33',
    #     'viewtitleName':'COLUMN312',
    #     'viewsubTitleName':'COLUMN310',
    #     }

    #重新读入代理
    if index % 1000 == 0:
        getTheRemoteAgent()

    # prepare = Request('POST', target_url, headers=headers, data=data).prepare()
    actUrl = target_url % index
    print actUrl
    prepare = Request('GET', actUrl, headers=headers).prepare()
    # try多次
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            index = random.randint(0, len(IPANDPORT)-1)
            proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
            print proxy
            result = session.send(prepare, timeout=20, verify=False)
            success = True
        except Exception, e:
            print '请求失败, 重试...'
            print e
            attempts += 1
            if attempts==3:
                print '请求三次失败,跳过'
                pass
    # prase(result.text)
    praseJson(result.text)

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
    print '录入中...'
    path = os.path.expanduser(r'~/Desktop/test/test50000-100000.txt')
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
getTheRemoteAgent()
pool = Pool(10)
for index in range(50000,100000):
    host = 'http://api.doctorpda.cn/api/u/profile?id=%s&follow=1&ext=true'
    pool.apply_async(getNextUrl, args=(host, index))
pool.close()
pool.join()
print 'All subprocesses done.'
