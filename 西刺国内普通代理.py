#!/usr/bin/env python
#coding:utf-8
import urllib2, urllib
import re
import threading
import time
from bs4 import BeautifulSoup

rawProxyList = []
checkedProxyList = []

#抓取代{过}{滤}理网站
targets = []
for i in xrange(1,2):
    if i != 1:
        target = r"http://www.xicidaili.com/nt/%d" % i
        targets.append(target)
    else:
        target = r"http://www.xicidaili.com/nt/"
        targets.append(target)
#print targets
print targets

#获取代{过}{滤}理的类
class ProxyGet(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self)
        self.target = target

    def getProxy(self):
        print "目标网站： " + self.target
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = { 'User-Agent' : user_agent }

        req = urllib2.Request(self.target, headers = header)
        req = urllib2.urlopen(req)
        result = req.read()

        soup = BeautifulSoup(result, 'lxml')
        for child in soup.find_all('tr'):
            result = child.find_all('td')
            proxy = []
            try:
                proxy = [result[2].string.encode('utf8'),result[3].string.encode('utf8')]
            except:
                pass
            #print proxy
            print proxy
            rawProxyList.append(proxy)

    def run(self):
        self.getProxy()

#检验代{过}{滤}理的类
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        self.testStr = "030173"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            print proxy
            try:
                proxyHandler = urllib2.ProxyHandler({"http" : r'%s:%s' %(proxy[0],proxy[1])})
            #print r'http://%s:%s' %(proxy[0],proxy[1])
            except:
                pass
            opener = urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            #urllib2.install_opener(opener)
            t1 = time.time()

            try:
                #req = urllib2.urlopen("http://www.baidu.com", timeout=self.timeout)
                req = opener.open(self.testUrl, timeout=self.timeout)
                #print "urlopen is ok...."
                result = req.read()
                #print "read html...."
                timeused = time.time() - t1
                pos = result.find(self.testStr)
                #print "pos is %s" %pos

                if pos > 1:
                    checkedProxyList.append((proxy[0],proxy[1],timeused))
                    #print "ok ip: %s %s %s %s" %(proxy[0],proxy[1],proxy[2],timeused)
                else:
                    continue
            except Exception,e:
                #print e.message
                continue

    def run(self):
        self.checkProxy()

if __name__ == "__main__":
    getThreads = []
    checkThreads = []

#对每个目标网站开启一个线程负责抓取代{过}{滤}理
for i in targets:
    t = ProxyGet(i)
    getThreads.append(t)

for i in getThreads:
    i.start()

for i in getThreads:
    i.join()

print '.'*10+"总共抓取了%s个代{过}{滤}理" %len(rawProxyList) +'.'*10

#开启20个线程负责校验，将抓取到的代{过}{滤}理分成20份，每个线程校验一份
for i in range(20):
    t = ProxyCheck(rawProxyList[((len(rawProxyList)+19)/20) * i:((len(rawProxyList)+19)/20) * (i+1)])
    checkThreads.append(t)

for i in checkThreads:
    i.start()

for i in checkThreads:
    i.join()

print '.'*10+"总共有%s个代{过}{滤}理通过校验" %len(checkedProxyList) +'.'*10

#持久化
f= open("proxy_list2.txt",'a')
for proxy in sorted(checkedProxyList,cmp=lambda x,y:cmp(x[2],y[2])):
    print "checked proxy is: %s:%s" %(proxy[0],proxy[1])
    f.write("%s:%s\n"%(proxy[0],proxy[1]))
f.close()