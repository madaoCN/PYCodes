#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time
import Queue

import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import pymysql,random
import pymongo
import re

SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 3  #设置线程的个数

BASE_URL = 'http://sns.sseinfo.com/'
session = Session()
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
LASTID = None

class MyThread(threading.Thread) :
    """
    doc of class
    Attributess:
        func: 线程函数逻辑
    """
    def __init__(self, func) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑
    def run(self) :
        """
        重写基类的run方法
        """
        self.func()

def do_something(realUrl) :
    """
    运行逻辑, 比如抓站
    """
    import getRemoteAgent

    proxy = {'http': 'http://%s' % getRemoteAgent.getRandomRemoteAgent().strip()}
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        "cache-control": "max-age=0",
        'Connection': 'keep-alive',
        'Host': 'sns.sseinfo.com',
        'Referer': 'http://sns.sseinfo.com/qa.do',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept': 'text/html, */*; q=0.01',
        # 'X-Requested-With':'XMLHttpRequest',
        # 'Cookie':'''SSESNSXMLSID=da203d75-3d85-4f7c-bfc5-50eef8e78878; JSESSIONID=ozpp6s9j8e6cpu405s2prqn3'''
    }
    data = {}
    print proxy

    prepare = Request('GET', realUrl, headers=headers).prepare()
    try:
        result = session.send(prepare, proxies=proxy)
        # result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        conn.test.fails.insert({'url': target_url})
        return

    # collections = conn.test.html
    # print collections.insert({'html':result.text})

    print 'prasing.......'
    prase(prepare.text, realUrl)

def prase(text, tartget_url):
    '''
    '''
    soup = BeautifulSoup(text, 'lxml')
    #单项数据集合
    try:
        feedItems = soup.find_all('div', {'class':'m_feed_item'})
    except Exception, e:
        print e
        print '错误发生在prase feeditems解析'
        conn.test.fails.insert({'url': target_url})

    for item in feedItems:
        try:
            # 提问者
            ask = item.find('div', {'class':'m_feed_detail m_qa_detail'})
            askMan = ask.find('div', {'class':'m_feed_face'}).p.text.strip()
            askContent = ask.find('div', {'class':'m_feed_txt'}).text.strip()
            #回答者
            answer = item.find('div', {'class':'m_feed_detail m_qa'})
            answerMan = answer.find('div', {'class':'m_feed_face'}).p.text.strip()
            answerContent = answer.find('div', {'class':'m_feed_txt'}).text.strip()
            #id
            _id = item['id'].strip('item-')
            #时间
            time = item.find('div',{'class':'m_feed_from'}).span.text
            global LASTID
            LASTID = _id
        except Exception, e:
            print '错误发生在prase item解析'
            print e
            conn.test.fails.insert({'url': target_url})
        break

    print 'load to db.....'

    dic = {'askMan': askMan.encode('utf8'),
           'askContent': askContent.encode('utf8'),
           'answerMan': answerMan.encode('utf8'),
           'answerContent': answerContent.encode('utf8'),
           'time':time.encode('utf8')}

    try:
        db = conn.test
        collections = db.DATA
        collections.insert(dic)
    except Exception as e:
        print 'prase 数据库录入失败'
        conn.test.fails.insert({'url': tartget_url})
        print e
    print '数据录入mongo...'

def worker() :
    """
    主要用来写工作逻辑, 只要队列不空持续处理
    队列为空时, 检查队列, 由于Queue中已经包含了wait,
    notify和锁, 所以不需要在取任务或者放任务的时候加锁解锁
    """
    global SHARE_Q
    while True :
        if not SHARE_Q.empty():
            item = SHARE_Q.get() #获得任务
            do_something(item)
            time.sleep(1)
            SHARE_Q.task_done()

def main() :
    global SHARE_Q
    threads = []
    #向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    # for task in xrange(5) :
    #     print task
    #     SHARE_Q.put(task)
    while 1:
        url = conn.test.fails.find_one()['url']
        print '从fail库中取得url:' + url
        SHARE_Q.put(url)
    #开启_WORKER_THREAD_NUM个线程
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()  #线程开始处理任务
        threads.append(thread)
    for thread in threads :
        thread.join()
    #等待所有任务完成
    SHARE_Q.join()

if __name__ == '__main__':
    main()