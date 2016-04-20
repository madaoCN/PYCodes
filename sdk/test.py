#!/usr/bin/env python
#coding=utf-8
import re

baseUrl = 'http://api.doctorpda.cn'
raw = '''POST /api/v2/case/index?app_key=f1c18i2otirc0004&client_id=0bd1agocekr6073a&access_token=c83ad482-b05c-4187-9c07-566454b0b168&net=wifi&versionName=4.2.2&versionCode=85&source=app HTTP/1.1
Host: api.doctorpda.cn
Content-Type: application/x-www-form-urlencoded
Accept: */*
Connection: keep-alive
Cookie: JSESSIONID=5D676C5FFC64A8A1F6970744275F6A32; JSESSIONID=5D676C5FFC64A8A1F6970744275F6A32; login_id=15221131593; secret_token=84bc894eada38d0b24fbcfd6163b914b
User-Agent: new_doctorpda/4.2.2 (iPhone; iOS 9.2; Scale/2.00) doctorpda
Accept-Language: zh-Hans-CN;q=1
Accept-Encoding: gzip, deflate
Content-Length: 51

data=sQh4bt25KD2cdxQlfrrOkFBPumJn2HZ44hqH7hAfubk%3D
'''


def assign(service, arg):
    if service == "MDPost":
        return True, arg

# 主体攻击代码
def audit(arg):
    try:
        code, head, body, errcode, final_url = curl.curl2(arg, raw)
    except Exception, e:
        print e
    # 输出错误信息
    outPutErrInfo(code, head, body, errcode, final_url)


# 输出错误信息
def outPutErrInfo(code, head, body, errcode, final_url):
    # 以下显示HTTP状态码
    print'---------------HTTPcode---------------'
    print code
    # 以下显示HTTP头
    print'---------------HTTPHead---------------'
    print head
    # 以下显示HTTP主体内容(HTML)
    print'---------------HTTPBody---------------'
    print body
    # 以下显示curl的状态码
    print'-------------err code-------------'
    print errcode
    # 以下显示curl访问的URL
    print'------------final_url-------------'
    print final_url

if __name__ == '__main__':
    from dummy import *
    audit(assign('MDPost', baseUrl)[1])
