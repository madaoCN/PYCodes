#coding=utf-8
import requests
from requests import Request, Session
import re
import os
import random
session = Session()
IPANDPORT = []
# 获取代理列表
def getTheRemoteAgent():
    desktopPath = os.path.join(os.path.expanduser("~"), 'Desktop')
    f = open(desktopPath + '/' + 'proxy_list.txt', "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def run(date):
    #construct page
    realUrl = 'http://sns.sseinfo.com/getNewDataCount.do'

    index = random.randint(0, len(IPANDPORT)-1)
    proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
    print proxy
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # "cache-control": "max-age=0",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Host': 'sns.sseinfo.com',
        'Origin': 'http://sns.sseinfo.com',
        'Referer': 'http://sns.sseinfo.com/qa.do',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        # 'Cookie':'SSESNSXMLSID=da203d75-3d85-4f7c-bfc5-50eef8e78878; JSESSIONID=1a6093syen5w81d361g14gjx61'
        # 'Cookie':'''SSESNSXMLSID=da203d75-3d85-4f7c-bfc5-50eef8e78878; JSESSIONID=ozpp6s9j8e6cpu405s2prqn3'''
    }
    data = {
        # 'sdate': startTime,
        # 'edate':endTime,
        'sdate': date,
        'edate': date,
        'type': '1',
        'keyword': '',
        'comid': ''
    }


    prepare = Request('POST', realUrl, headers=headers, data=data).prepare()
    try:
        result = session.send(prepare, proxies=proxy, timeout=5)
        # result = session.send(prepare, timeout=10)
        print date
        print result.text
        return result.text
    except Exception, e:
        print '请求失败'
        return

getTheRemoteAgent()
run('2016-01-19')
