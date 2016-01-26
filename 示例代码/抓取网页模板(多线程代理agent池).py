#coding=utf-8
import urllib
import urllib2
import cookielib
import string
import json, codecs, csv
import requests, random, time, codecs, threading, re
from bs4 import BeautifulSoup

class Spider(threading.Thread):
    def __init__(self, baseUrlList):
        threading.Thread.__init__(self)
        self.baseUrlList = baseUrlList

    #  # 构造请求参数
    # def constructPostData(self):
    #     postData = {'tokenId':'180A392E6E6C94C92AC1DCBA48A6AC8DB'}
    #     # self.dataTag += 1
    #     return postData

    #获得代理列表
    def getRandomAgent(self):
        agent = []
        with codecs.open('proxy_list.txt', 'rb', "utf-8") as f:
            # 获取文件行数
            for line in f:
                agent.append(line)

        return agent
    # 获得浏览器头列表
    def getRandomWebBrowser(self):
        agent = []
        with codecs.open('webBrowser.txt', 'rb', "utf-8") as f:
            # 获取文件行数
            for line in f:
                agent.append(line.strip(' ').strip('"').strip('\n'))
        return agent


    # 获得页面数据
    def getPage(self, targetUrl):
        #使用代理
        proxys = self.getRandomAgent()
        random.seed(time.time())
        index = random.randint(0, len(proxys)-1)
        ipANDport  = proxys[index]

        # 使用随机头
        agent = self.getRandomWebBrowser()
        random.seed(time.time())
        index = random.randint(0, len(agent)-1)
        broswerHead  = agent[index]

        print ipANDport
        print broswerHead

        handler = urllib2.ProxyHandler({'http':ipANDport})
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        opener.addheaders = [('User-agent', broswerHead)]

        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
            # # 返回页面数据
            # session = requests.Session()
            # response = session.post(self.baseUrl, _data, self.headers, )
            # return response.text
                result = opener.open(targetUrl)
                self.dealWithResult(result)
                success = True
        # 捕获异常
            except urllib2.HTTPError, e:
                if hasattr(e,"code"):
                    print e.code
                if hasattr(e,"reason"):
                    print e.reason
                attempts += 1
	            if attempts==3:
                    pass
        # # 捕获异常
        # except urllib2.URLError, e:
        #     if hasattr(e,"code"):
        #         print e.code
        #     if hasattr(e,"reason"):
        #         print e.reason

    # 处理字符(删除\n \t \r)
    # def dealWithString(self, response):
    #     jsonStr = json.loads(response)
    #     jsonData = json.dumps(jsonStr['html'], ensure_ascii=False, indent=2)
    #     return jsonData

    #处理结果
    def dealWithResult(self, result):
        soup = BeautifulSoup(result, 'lxml')
        table = soup.find("table")
        for tr in table.find_all('tr'):
            result = tr.find_all('td')
            # 产品编号
            no = result[0].find('span').string.encode('utf-8')
            # 产品名称
            name = result[1].find('a').string.encode('utf-8')
            # 产品链接地址
            nameUrl = result[1].find('a')['href'].encode('utf-8')
            # 规格
            category = result[2].string.encode('utf-8')
            # 单价
            price = result[4].span.string.strip().encode('utf-8').split('元')[0]
            self.writeToFile(no, name, nameUrl, category, price)
    # 写入文件
    def writeToFile(self, *args):
        arr = []
        for arg in args:
            temp = arg.decode('utf-8').encode('gbk', 'ignore')
            arr.append(temp)
            print temp
        with codecs.open('test.csv', 'a', 'gbk') as file:
            writer = csv.writer(file)
            writer.writerow(arr)

    # 开始方法
    def run(self):
        for url in self.baseUrlList:
            self.getPage(url)



if __name__ == "__main__":
    baseUrl = '''http://www.bio-city.net/index.php/Search/index/search_gys/3/p/%s'''
    getThreads = []
    urlList = []

# 拼接地址
for i in range(1025):
    if i == 0:
        url = baseUrl % ""
    else:
        url = baseUrl % i
    urlList.append(url)
# 把地址分成20份
for i in range(20):
    t = Spider(urlList[((len(urlList)+19)/20)*i : ((len(urlList)+19)/20)*(i+1)])
    getThreads.append(t)

for i in getThreads:
    i.start()

for i in getThreads:
    i.join()




