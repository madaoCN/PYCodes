#coding=utf-8
import urllib
import urllib2
import cookielib

# 对象实例来保存cookie
myCookie = cookielib.CookieJar()
# 创建cookie处理器
handler = urllib2.HTTPCookieProcessor(myCookie)
# cookie处理器来初始化一个opener
myOpner = urllib2.build_opener(handler)
# 输出cookie
for item in myCookie:
    print "name=" + item.name
    print "value=" + item.value

# 保存cookie到文件
#设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#创建一个请求，原理同urllib2的urlopen
response = opener.open("http://www.baidu.com")
#保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)


# 文件中获取cookie并访问
#创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()
#从文件中读取cookie内容到变量
cookie.load("cookie.txt", ignore_expires=True, ignore_discard=True)
#创建请求的request
req = urllib2.Request("http://www.baidu.com")
#利用urllib2的build_opener方法创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()

