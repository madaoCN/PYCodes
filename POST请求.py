#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import re

IPANDPORT = []
TARGET_HOST = 'https://gw.wmcloud.com/datamkt/orderSetup?lang=zh'
session = Session()


def run_pro(target_url):
    #construct page
    realUrl = target_url

    headers = {
        'cookie':'cloud-anonymous-token=d1d857b29c4245c89023b37e7ac2266a; cloud-sso-token=0EA76431CB154F1337B19C433434E79D',
        'accept':'application/json;charset=utf-8',
        'accept-encoding': 'gzip, deflate, br',
    # 'accept - language':'zh - CN, zh;q = '0.8'
        'content-type':'application/json;charset=UTF-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
        'origin': 'https://mall.datayes.com',
        'referer':'https://mall.datayes.com/order?lang=zh'
    }
    dataDic = {"goods":[{"id":105,"num":3}],"totalPrice":0}

    prepare = Request('POST', realUrl, headers=headers, data=dataDic).prepare()
    try:
        # result = session.send(prepare, proxies=proxy)
        result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        return
    print 'prasing.......'
    print result.text
    # prase(result.text)



if __name__ == '__main__':
    run_pro(TARGET_HOST)


print 'All subprocesses done.'
