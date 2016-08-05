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
LASTID = None
TARGET_HOST = 'http://sns.sseinfo.com/ajax/feeds.do?type=11&pageSize=10'
session = Session()
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)

# 获取代理列表
def getTheRemoteAgent():
    desktopPath = os.path.join(os.path.expanduser("~"), 'Desktop')
    f = open(desktopPath + '/' + 'proxy_list.txt', "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

def run_pro(target_url, page):
    #construct page
    realUrl = target_url
    realUrl = target_url + '&lastid=-1&show=1&page=%s' % (page+1,)

    print realUrl
    index = random.randint(0, len(IPANDPORT)-1)
    proxy = {'http':'http://%s' % IPANDPORT[index].strip()}
    headers = {
        'Accept':'*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        "cache-control": "max-age=0",
        'Connection':'keep-alive',
        'Host': 'sns.sseinfo.com',
        'Referer': 'http://sns.sseinfo.com/qa.do',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept':'text/html, */*; q=0.01',
        'X-Requested-With':'XMLHttpRequest',
               # 'Cookie':'''SSESNSXMLSID=da203d75-3d85-4f7c-bfc5-50eef8e78878; JSESSIONID=ozpp6s9j8e6cpu405s2prqn3'''
    }
    data = {}
    print proxy

    prepare = Request('GET', realUrl, headers=headers).prepare()
    try:
        # result = session.send(prepare, proxies=proxy, timeout=5)
        result = session.send(prepare, timeout=10)
        print 'connect'
        if result == None:
            conn.test.fails.insert({'url': target_url})
        collections = conn.test.html
        # print collections.insert({'html':result.text})
        # html = collections.find_one()
        print 'prasing.......'
        prase(result.text, realUrl)
    except Exception, e:
        print '请求失败'
        print e
        if conn.test.DATA.find_one({'url': realUrl}) == None:
            conn.test.fails.insert({'url': realUrl})
        return

def prase(text, realUrl):
    '''
    '''
    soup = BeautifulSoup(text, 'lxml')
    #单项数据集合
    try:
        feedItems = soup.find_all('div', {'class':'m_feed_item'})
    except Exception, e:
        print e
        print "抓取网页失败"
        if conn.test.DATA.find_one({'url': realUrl}) == None:
            conn.test.fails.insert({'url': realUrl})
        return

    for item in feedItems:
        try:
            ask = item.find('div', {'class':'m_feed_detail m_qa_detail'})
            #提问人
            askMan = ask.find('div', {'class':'m_feed_face'}).p.text.strip()
            #提问内容
            askContent = ask.find('div', {'class':'m_feed_txt'}).contents[2].strip()
            #提问时间
            askTime = ask.find('div',{'class':'m_feed_from'}).span.text.strip(r'"()"')

            answer = item.find('div', {'class':'m_feed_detail m_qa'})
            #上市公司
            answerMan = answer.find('div', {'class':'m_feed_face'}).p.text.strip()
            #上市公司代码
            patt = re.compile(r"\((.*?)\)", re.I | re.X)
            answerID = patt.findall(ask.find('div', {'class':'m_feed_txt'}).a.text.strip())[0]
            #上市公司回答内容
            answerContent = answer.find('div', {'class':'m_feed_txt'}).text.strip()
            #上市公司回答时间
            answerTime = answer.find('div',{'class':'m_feed_from'}).span.text.strip(r'"()"')

            #id
            # _id = item['id'].strip('item-')
            #时间
            # time = item.find('div',{'class':'m_feed_from'}).span.text
            #点赞数
            # praiseNum = item.find('div',{'class':'m_feed_handle'}).a.text.strip(r'"()"')
            try:
                dic = {'askMan': askMan.encode('utf8'),
                       'askContent': askContent.encode('utf8'),
                       'askTime': askTime.encode('utf8'),
                       'answerMan': answerMan.encode('utf8'),
                       'answerID':answerID.encode('utf8'),
                       'answerContent': answerContent.encode('utf8'),
                       'answerTime': answerTime.encode('utf8')}
            except Exception, e:
                print e

            print '数据录入mongo...'
            try:
                db = conn.test
                collections = db.DATA
                collections.insert(dic)
            except Exception as e:
                print 'prase 数据库录入失败'
                print e
                continue
        except Exception, e:
            print '错误发生在prase item解析'
            print e
            continue


    print 'load to db.....'


# if __name__ == '__name__':
getTheRemoteAgent()
# print IPANDPORT
pool = Pool(5)
for index in range(0, 10):
    pool.apply_async(run_pro, args=(TARGET_HOST, index))
pool.close()
pool.join()
conn.close()


print 'All subprocesses done.'
