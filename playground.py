# coding=utf-8
import re
import os
import urllib, urllib2
from bs4 import BeautifulSoup
import chardet


target = 'http://www.baidu.com'
req = urllib2.Request(target)
response = urllib2.urlopen(req)
content = response.read()
content = content.decode('utf8')

print content
soup = BeautifulSoup(content, 'lxml')

a = soup.find_all('a', {'name':'tj_trnuomi'})
# print a[0].text





