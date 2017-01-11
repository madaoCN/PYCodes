#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import re

IPANDPORT = []
TARGET_HOST = 'http://ft.10jqka.com.cn/thsft/iFindService/f9Stock/stock110?thscode=%s'
session = Session()


def run_pro(target_url, line):
    #construct page
    realUrl = target_url
    print realUrl
    headers = {
        'Accept - Encoding': 'gzip, deflate',
        'cookie':'THSFT_USERID=shjtdx001;jgbsessid=ea7eafe01ddea6dcd3b496cca1816c81;mid=MDgtMDAtMjctOTAtODktNjQ =;Version = iFinD/1.10.12.300_148503591',
        'accept':'*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'content-type':'application/json;charset=UTF-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        'user-agent':'iFinD/1.10.12.300_148503591',
        # 'host':'ft.10jqka.com.cn'
    }
    # dataDic = {"goods":[{"id":105,"num":3}],"totalPrice":0}

    prepare = Request('GET', realUrl, headers=headers).prepare()
    try:
        # result = session.send(prepare, proxies=proxy)
        result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        return
    print 'prasing.......'
    # print result.text
    # prase(result.text)
    if len(result.text) > 0:
        with codecs.open('/Users/liangxiansong/Desktop/out/%s' % line + '.txt', 'w+') as file:
            file.write(result.text.encode('utf8'))




if __name__ == '__main__':
    # run_pro(TARGET_HOST)
    import codecs
    with codecs.open('/Users/liangxiansong/Desktop/ids.txt', 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            run_pro(TARGET_HOST % line, line)

print 'All subprocesses done.'
