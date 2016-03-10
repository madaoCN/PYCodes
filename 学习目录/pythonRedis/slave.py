import urllib2
from RedisQueue import RedisQueue
redis = RedisQueue('jandan3')

def user_agent(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0
''}
    req_timeout = 20
    req = urllib2.Request(url,None,req_header)
    page = urllib2.urlopen(req,None,req_timeout)
    html = page
    return html

while not redis.empty():
    down_url = redis.get()
    data = user_agent(down_url).read()
    with open('/mz/picture'+'/'+down_url[-11:],'wb')as code:
        code.write(data)
    print down_url