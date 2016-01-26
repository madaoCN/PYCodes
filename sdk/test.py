#!/usr/bin/env python
#coding=utf-8
import re

baseUrl = 'http://app.wy.guahao.com/checklogin'
raw = '''GET /checklogin?to=http%3A%2F%2Fapp.wy.guahao.com%2Fstandardepartment%2F7f67f180-cff3-11e1-831f-5cf9dd2e7135&token= HTTP/1.1
Host: app.wy.guahao.com
Accept-Encoding: gzip, deflate
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Cookie: _wysid_=145208767747220178067201
Connection: keep-alive
Accept-Language: zh-cn
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13B143 MWYBrowser/2.3.9
'''


def assign(service, arg):
    if service == "MDPost":
        return True, arg

# 主体攻击代码
def audit(arg):
    code, head, body, errcode, final_url = curl.curl2(arg, raw)
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
