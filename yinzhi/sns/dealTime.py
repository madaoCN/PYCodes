#coding=utf-8
import re
import pymongo
import reverseDay

def dealTime(str, year):
    stri = str.encode('utf8')
    year = year.encode('utf8')
    #判断是否是 XXX 小时前
    hourPat = re.compile(r'小时前')
    #判断是否是有 昨天
    yesterPat = re.compile(r'昨天')
    #判断是否有 xxx分钟前
    minutePat = re.compile(r'分钟前')

    if hourPat.search(stri):
        return '2016年08月05日'
    elif yesterPat.search(stri):
        return '2016年08月04日'
    elif minutePat.search(stri):
        return '2016年08月05日'
    else:
        # return str(year)+'年'+ stri.encode('utf8').split('')[0]
        try:
            return  year +'年'+stri.split(' ')[0]
        except Exception, e:
            print 'error at dealTime 年'
            print e


# for i in reverseDay.getDate():
#     print dealTime(u'分钟前', i.split('-')[0])
