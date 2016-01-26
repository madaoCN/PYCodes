#coding=utf-8
import urllib
import urllib2
import cookielib
import string
import json
import requests, random, time, codecs, threading, pymysql, re
from bs4 import BeautifulSoup


conn=pymysql.connect(host='localhost',user='root',passwd='123456',port=3306,charset='utf8')
cur=conn.cursor()


class Spider(object):
    def __init__(self):
        self.baseUrl = '''http://www.bio-city.net/index.php/Search/index/search_gys/3/p/8'''

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
    def getPage(self):
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

        handler = urllib2.ProxyHandler({'http':ipANDport})
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        opener.addheaders = [('User-agent', broswerHead)]
        try:
            # # 返回页面数据
            # session = requests.Session()
            # response = session.post(self.baseUrl, _data, self.headers, )
            # return response.text
            result = opener.open(self.baseUrl)
            self.dealWithResult(result)

        # 捕获异常
        except urllib2.HTTPError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
        # 捕获异常
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason

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
            self.writeToFile(int(no), name, nameUrl, category, float(price))
    # 写入文件
    def writeToFile(self, *args):
        for arg in args:
            print arg
        cur.execute("USE test15")
        # cur.execute("INSERT INTO TEST VALUES(%s , %s, %s, %s, %s)" % (args[0], args[1], args[2], args[3], args[4]))
        cur.execute("INSERT INTO test15 VALUES(1 , 'asf', 'sdfxc', 'sdf', 3.0)")
        print cur.fetchone()


    def createSQLTable(self):
        cur.execute("CREATE DATABASE test15")
        # cur.execute("DROP TABLE IF EXISTS TEST")
        cur.execute("USE test15")
        sql = '''
         CREATE TABLE test15 (
         no  INT NOT NULL,
         name  CHAR(50),
         url CHAR(50),
         category CHAR(50),
         price FLOAT)
        '''
        cur.execute(sql)
        print cur.fetchone()

    # 开始方法
    def start(self):
        print self.baseUrl
        # self.createSQLTable()
        self.getPage()
        cur.close()
        conn.close()


spider = Spider()
spider.start()
