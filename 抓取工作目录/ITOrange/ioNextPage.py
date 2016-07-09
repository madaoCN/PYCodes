#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random
import pymongo
import re

IPANDPORT = []
TARGET_HOST = 'http://www.itjuzi.com/company?scope=47'
session = Session()
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)

# 获取代理列表
def getTheRemoteAgent():
    f = open("/Users/liangxiansong/Desktop/proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def run_pro(target_url):
    index = random.randint(0, len(IPANDPORT)-1)
    proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
               "cache-control":"no-cache",
               "Content-Type":"application/x-www-form-urlencoded",
               'Host': 'www.itjuzi.com',
               'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8Accept - Encoding:gzip, deflate, sdch',
               'Accept - Language': 'zh - CN, zh;q = 0.8',
               'Cookie':'''gr_user_id=db2b0d52-2903-4fc4-8608-7fbe9141e6d2; gr_session_id_eee5a46c52000d401f969f4535bdaa78=20dc3403-055f-4a06-a1ff-c6e51bfde896'''
    }
    data = {}
    print proxy
    print target_url

    prepare = Request('GET', target_url, headers=headers).prepare()
    try:
        # result = session.send(prepare, proxies=proxy, timeout=10)
        result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        conn.test.fails.insert({'url':target_url})
        return

    # collections = conn.test.html
    # print collections.insert({'html':result.text})
    print 'prasing.......'
    prase(result.text, target_url)

    # html = conn.test.html.find_one()
    # prase(html['html'], target_url)

def prase(text, tartget_url):
    '''
    '''
    soup = BeautifulSoup(text, 'lxml')
    div = soup.find_all('div', {'class':'line-title'})
    span = div[0].find('span',  {'class':'title'})
    project = span.b.contents[0].strip()#项目名称
    project = ''.join(span.b.contents[0].strip().split('\t'))

    span = soup.find('span', {'class':'loca c-gray-aset'})
    area = span.contents[-2].text#地区

    a = soup.find('a', {'class':'weblink marl10'})
    link = a['href']  # 公司网站

    div = soup.find('div', {'class':'des-more'})
    companyName = div.contents[1].span.text.strip()
    companyName = companyName[5:]#公司名称

    div = soup.find_all('div', {'class':'des'})
    introduct = div[0].text.strip() #公司简介

    div = soup.find('div', {'class': 'des-more'})
    time = div.contents[3].span.text.strip()#成立时间
    time = time[5:]

    dic = {'project': project.encode('utf8'),
           'area': area.encode('utf8'),
           'link': link.encode('utf8'),
           'companyName': companyName.encode('utf8'),
           'introduct': introduct.encode('utf8'),
           'time': time.encode('utf8'),}

    #遍历融资信息
    list = []
    table = soup.find('table', {'class':'list-round-v2'})
    if table:#存在融资信息
        trs = table.contents[1:-1]
        for tr in trs:
            try:
                rounds = tr.find('span',{'class':'round'}).a.text
                finades = tr.find('span',{'class':'finades'}).a.text
                result = rounds+':'+finades
                list.append(result.strip().encode('utf8'))
            except Exception as e:
                continue
    #录入数据库
    dic['round'] = list

    try:
        db = conn.test
        collections = db.DATA
        collections.insert(dic)
    except Exception as e:
        print 'prase 数据库录入失败'
        conn.test.fails.insert({'url': tartget_url})
        print e
    print '数据录入mongo...'

    # for url in URLS:
    #     print url
    #     db = conn.itJuZi
    #     collections = db.URLS
    #     collections.insert({'url':url})是
    # print 'load to db.....'

# if __name__ == '__name__':
getTheRemoteAgent()
# print IPANDPORT
pool = Pool(5)
consur = conn.test.FAILS.find()
for item in consur:
    pool.apply_async(run_pro, args=(item['url'],))
pool.close()
pool.join()
conn.close()


print 'All subprocesses done.'
