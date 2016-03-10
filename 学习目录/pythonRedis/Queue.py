#coding=utf-8
from bs4 import BeautifulSoup
import urllib2
from Queue import Queue
from RedisQueue import RedisQueue
queue = Queue()
redis = RedisQueue('jandan3')

def user_agent(url):
    req_header = {'User-Agent‘':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}
    req_timeout = 20
    req = urllib2.Request(url,None,req_header)
    page = urllib2.urlopen(req,None,req_timeout)
    html = page
    return html

def next_page():
    base_url = 'http://jandan.net/ooxx/page-1006#comments'
    for i in range(3):
        html = user_agent(base_url).read()
        soup = BeautifulSoup(html)
        next_url = soup.find('a',{'class':'next-comment-page','title':'Newer Comments'}).get('href')
        yield base_url
        base_url = next_url
for page in next_page():
    queue.put(page)
print 'There are %d pages'%queue.qsize()

while not queue.empty():
    page_url = queue.get()
    html = user_agent(page_url).read()
    soup = BeautifulSoup(html)
    img_urls = soup.find_all(['img'])
    for myimg in img_urls:
        Jpgurl = myimg.get('src')
        redis.put(Jpgurl)
print 'There are %d pictures'%redis.qsize()