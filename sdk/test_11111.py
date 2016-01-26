#!/usr/bin/env python
#coding=utf-8
import re

baseUrl = 'http://consult.cdfortis.com:8088/appService/appTwo!searchDoctorByKey.action'
raw='''POST http://consult.cdfortis.com:8088/appService/appTwo!searchDoctorByKey.action HTTP/1.1
Content-Type: text/html
Cache-Control: no-cache
Charsert: UTF-8
Cookie: JSESSIONID=C0D1CDE04700BD479DE3C3FE4D9DD81A.app2; Path=/appService/; HttpOnly
User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.1.2; MI 1S MIUI/JMACNBL18.0)
Host: consult.cdfortis.com:8088
Connection: Keep-Alive
Accept-Encoding: gzip
Content-Length: 119

{"longitude":119.301423,"tokenId":"14E629CAE9C934B04A82A0DB26D6C5D1C","latitude":26.076827,"type":1,"page":1,"rows":15}'''

def assign(service, arg):
    if service == "MDPost":
        return True, arg

# 主体攻击代码
def audit(arg):
    rawHTTPReq = raw
     # 获取Content-Length参数长度
    pattern_1 = re.compile(r'{.*?}')
    match_1 = re.findall(pattern, string)
    print match_1
    print len(match_1[0])
    # 获取content——length长度
    pattern = re.compile(r':\s\d+')
    match = re.findall(pattern, string)
    print match
    result, number = re.subn(pattern, ': '+len(match_1[0]), string)
    print result

    code, head, body, errcode, final_url = curl.curl2(arg,raw=rawHTTPReq)
    print body
    # 输出错误信息
    # outPutErrInfo(code, head, body, errcode, final_url)

# 输出错误信息
def outPutErrInfo(code, head, body, errcode, final_url):
    # 以下显示HTTP状态码
    print'---------------HTTPcode---------------'
    print code
    # 以下显示HTTP头
    print'---------------HTTPHead---------------'
    print head
    # 以下显示HTTP主体内容(HTML)
    # print'---------------HTTPBody---------------'
    # print body
    # 以下显示curl的状态码
    print'-------------err code-------------'
    print errcode
    # 以下显示curl访问的URL
    print'------------final_url-------------'
    print final_url

if __name__ == '__main__':
    from dummy import *
    audit(assign('MDPost', baseUrl)[1])
