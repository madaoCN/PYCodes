#coding=utf8
import requests
from requests import Session, Request
import lxml
from bs4 import BeautifulSoup
import pymongo

BASE_URL = 'https://www.sec.gov/Archives/edgar/monthly/'
conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
consur = conn.secCom


# def prasePage(text):
#     soup = BeautifulSoup(text, 'lxml')
#     table = soup.find('table', {'summary':'heding'})
#     aItems = table.find_all('a')
#     for a in  aItems:
#         try:
#             consur.xmlPath.insert({'xmlPath':BASE_URL + a['href']})
#         except Exception, e:
#             print '录入数据库错误'
#             print e
#
# session = Session()
# prepare = Request('GET', BASE_URL).prepare()
# try:
#     # result = session.send(prepare, proxies=proxy, timeout=5)
#     result = session.send(prepare, timeout=10)
#     print 'connect'
#     # print 'prasing.......'
#     prasePage(result.text)
# except Exception, e:
#     print '请求失败'
#     print e


def downUrlRetrieve(url, fileName):
    '''
    下载URL
    '''
    print "downloading with requests"
    r = requests.get(url)
    import os
    desktopPath = os.path.join(os.path.expanduser("~"), 'Desktop/xmls/'+fileName)
    with open(desktopPath, "wb") as code:
        code.write(r.content)


