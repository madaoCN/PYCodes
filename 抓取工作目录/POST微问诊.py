#coding=utf-8
import urllib
import urllib2
import cookielib

baseUrl =  'http://consult.cdfortis.com:8088/appService/app!getStoreActivity.action'
headers = {'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.1.2; MI 1S MIUI/JMACNBL18.0)',
            'Connection': 'Keep-Alive',
           'Charsert': 'UTF-8',
           'Accept-Encoding': 'gzip',
           'Cache-Control': 'no-cache'
}
data = {'tokenId':'14E629CAE9C934B04A82A0DB26D6C5D1C'}

#设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
# urllib2安装opner
urllib2.install_opener(opener)
#创建一个请求，原理同urllib2的urlopen
reqData = urllib.urlencode(data)
handler = urllib2.Request(baseUrl, reqData, headers)

try:
    response = urllib2.urlopen(handler)
    print response.read()
    #保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)
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