#coding=utf-8
import urllib
import urllib2
import cookielib
import string
import json
from bs4 import BeautifulSoup

# # 请求头
# headers = {'User-Agent': 'android 4.1.2;867746015013717;zys 8.1.2;MI 1S zhjkyzYs safari webkit',
#            'X-Requested-With':'XMLHttpRequest'}
# # target地址
# baseUrl = "http://m.120ask.com/kuaiwen/site/doctor"

# 数据
# data = {'id':13599,'showwxpaytitle':1}

class Spider(object):
    def __init__(self):
        self.headers = {'User-Agent': 'new_doctorpda/4.2.2 (iPhone; iOS 9.3; Scale/2.00) doctorpda',
           'Cookie':'JSESSIONID=CE1D48E03C95B4D5D841F79AEE55B895; Hm_lvt_bc9d4fa6469686fe63002104880688b1=1460551175,1460717756; JSESSIONID=CE1D48E03C95B4D5D841F79AEE55B895; login_id=15221131593; secret_token=84bc894eada38d0b24fbcfd6163b914b'}
        self.data = {'data':'xCtl8j6pbBDaw53TMFbZMSDgBDoxuv57m9vj5INOfTU%3D'}
        self.baseUrl = 'http://api.doctorpda.cn/api/v2/case/index?app_key=f1c18i2otirc0004&client_id=7c01ag7q3qcc0112&access_token=72ba7500-7562-40a0-a17e-f3cb465e3839&net=wifi&versionName=4.2.2&versionCode=85&source=app '

     # 构造请求参数
    def constructPostData(self):
        postData = {'id':13599,'showwxpaytitle':1}
        # self.dataTag += 1
        return postData

    # 获得页面数据
    def getPage(self, _data):
        # post请求体编码
        req_data = urllib.urlencode(self.data)
        # 构造HTTP请求
        request = urllib2.Request(self.baseUrl, req_data, self.headers)
        print request
        # 发起post请求
        try:
            # 获的请求的句柄
            handler = urllib2.urlopen(request)
            # 返回页面数据
            print handler.read()
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
    def dealWithString(self, response):
        response_ = response.replace('\r','').replace('\t','').replace('\n','')
        jsonStr = json.loads(response_)
        jsonData = json.dumps(jsonStr['html'], ensure_ascii=False)

        soup = BeautifulSoup(jsonData, "lxml")
        return soup.find_all("span")

    # 写入文件
    def writeToFile(self):
        return None
    # 开始方法
    def start(self):
        pageData = self.getPage(self.constructPostData())
        # dataStr = self.dealWithString(pageData)
        # for data in dataStr:
        #     print data.string
        # print dataStr


spider = Spider()
spider.start()