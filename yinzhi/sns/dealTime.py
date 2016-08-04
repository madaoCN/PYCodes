#coding=utf-8
import re

def dealTime(stri, year):
    #判断是否是 XXX 小时前
    hourPat = re.compile(r'小时前')
    #判断是否是有 昨天
    yesterPat = re.compile(r'昨天')

    if hourPat.search(stri):
        return '2016年08月04日'
    elif yesterPat.search(stri):
        return '2016年08月03日'
    else:
        return str(year)+'年'+ stri
