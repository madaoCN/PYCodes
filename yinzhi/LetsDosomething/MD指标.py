#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import re
import codecs

IPANDPORT = []
TARGET_HOST = 'http://ft.10jqka.com.cn/thsft/dataservice'#上市时间表

session = Session()

def run_pro(target_url):
    #construct page
    realUrl = target_url
    print realUrl
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'cookie':'THSFT_USERID=shjtdx001;jgbsessid=32c6be0be91ddcd26b39de2e174f7d1e;mid=MDgtMDAtMjctOTAtODktNjQ=;Version=iFinD/1.10.12.300_148503591',
        'accept':'text/plain',
        'content-Type': 'application/x-www-form-urlencoded',
        # 'content-type':'application/json;charset=UTF-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        'user-agent':'iFinD/1.10.12.300_148503591',
        # 'host':'ft.10jqka.com.cn'
    }

    dataDic = {'xml_request':u'''<?xml version="1.0" encoding="gbk"?><request>
<items>
<item name="07198_000_00_0_6267"><params>
	<param name="FD" value="19930630" system="false"/>
	<param name="FN" value="100" system="true"/>
	<param name="单位大小" value="1" system=""/>
</params></item>
</items>
<thscodes>000001.SZ</thscodes>
</request>'''}

    prepare = Request('POST', realUrl, headers=headers, data=dataDic).prepare()
    try:
        # result = session.send(prepare, proxies=proxy)
        result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        return

    result.encoding = "gb2312"
    print result.headers
    print result.content
    print result.text
    if len(result.text) > 0:
        with codecs.open(u'/Users/liangxiansong/Desktop/out'  + '.txt', 'w+') as file:
            file.write(result.content)




if __name__ == '__main__':
    run_pro(TARGET_HOST)
    # import codecs
    # with codecs.open('/Users/liangxiansong/Desktop/ids.txt', 'r', 'utf8') as file:
    #     for line in file.readlines():
    #         line = line.strip()
    #         run_pro(TARGET_HOST % line, line)

print 'All subprocesses done.'
