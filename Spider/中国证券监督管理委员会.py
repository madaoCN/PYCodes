#coding=utf-8
from multiprocessing import Process, Pool
import os
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import random
import re
import chardet
import codecs
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

TARGET_HOST = 'http://www.csrc.gov.cn/pub/newsite/fxjgb/scgkfxfkyj/'
session = Session()
fileURLs = []

FILE = codecs.open(os.path.join(os.path.expanduser('~'), 'Desktop/files.txt'),'a', encoding='utf8')

def run_pro(target_url, page):
    #construct page
    realUrl = target_url
    if page != 0:
        realUrl = target_url + 'index_%s.html' % (page, )

    # print realUrl
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.csrc.gov.cn',
        'If-Modified-Since': 'Tue, 22 Nov 2016 10:10:00 GMT',
        'If-None-Match': '"5600000000b496-3344-541e0f9ad0529"',
        'Referer': 'http://www.csrc.gov.cn/pub/newsite/fxjgb/scgkfxfkyj/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
    }
    data = {}

    # print realUrl
    prepare = Request('GET', realUrl, headers=headers).prepare()
    # prepare = Request('GET', realUrl).prepare()

    try:
        # result = session.send(prepare, proxies=proxy)
        result = session.send(prepare)
    except Exception, e:
        print '请求失败'
        print e
        return
    # print 'prasing.......'
    prase(result.text.encode('ISO-8859-1'))

def getSecURL(targetURL):

    print 'targetURL',  targetURL
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        # 'Cache-Control':'max-age=0',
        'Content-Type':'text/html; charset=utf-8',
        # 'Connection':'keep-alive',
        # 'Host':'www.csrc.gov.cn',
        # 'If-Modified-Since':'Tue, 22 Nov 2016 10:10:00 GMT',
        # 'If-None-Match':'"5600000000b496-3344-541e0f9ad0529"',
        # 'Referer':'http://www.csrc.gov.cn/pub/newsite/fxjgb/scgkfxfkyj/',
        # 'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
        }
    prepare = Request('GET', targetURL, headers=headers).prepare()
    # prepare = Request('GET', targetURL).prepare()
    try:
        # result = session.send(prepare, proxies=proxy)
        result = session.send(prepare)

    except Exception, e:
        print '请求失败'
        print e
        return
    return result.text.encode('ISO-8859-1')

def getDocURL(html):

    try:
        result = re.search('''<a href="\./(.+?)\.doc(.*?)" .+?</a>''', html)
        if result == None:#文件链接为空
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('div', {'class':'title'})
            print title

            div = soup.find('div', {'class':'Custom_UnionStyle'})
            # print div.prettify()

            with codecs.open(os.path.join(os.path.expanduser('~'), 'Desktop/text/%s.txt' % title), 'a', encoding='utf8') as file:
                file.write(div.prettify())
            return

        result = result.group(0)
        url =  re.search('\./.+?\.doc.*?"',result).group(0).strip('"')
        name = re.search('>.+?\.doc.*?<', result).group(0).strip('>').strip('<')
        return url, name

    except Exception, e:
        print '解析失败'
        print e
    return None


def prase(text):
    '''处理HTML
    '''
    # print text
    try:
        soup = BeautifulSoup(text, 'lxml')
        aTags = soup.find_all('a')
        for aTag in aTags:
            href = aTag['href']
            if href.endswith('.html'):
                # firstURLs.append(href)
                print aTag['title'], href


                # try:
                #     html = getSecURL(TARGET_HOST + href.strip('./'))
                #     url, fileName =  getDocURL(html.encode('utf8'))
                #     if url or fileName:
                #         continue
                #     prefix = href.split('/')[1]
                #     print prefix + '/'+ url.strip('./') + '##' + fileName
                #     FILE.write(prefix + '/'+ url.strip('./') + '##' + fileName)
                #     FILE.write('\n')
                # except Exception, e:
                #     continue
                #     print e
                # global firstURLs
                # firstURLs.append(prefix + '/'+ url.strip('./') + '##' +fileName)

    except Exception , e:
        print e

    # aTags = div[2].find_all('a')
    # prog = re.compile(r"http://www.itjuzi.com/company/")
    # URLS = set()
    # for a in aTags:
    #     if prog.match(a['href']):
    #         url = a['href']
    #         URLS.add(url)
    #
    # for url in URLS:
    #     print url


def writeTofile(*arr):
    print arr
    path = os.path.expanduser(r'~/Desktop/data/test.txt' % (officeTemp))
    print path
    f = open(path, "a")
    if arr:
        for rag in arr:
            if isinstance(rag, int):
                f.write(str(rag)+',')
            else:
                f.write(rag.encode('UTF-8')+',')
        f.write('\n')
        f.close()


# if __name__ == '__name__':
# print IPANDPORT
pool = Pool(1)
for index in range(0, 20):
    pool.apply_async(run_pro, args=(TARGET_HOST, index))
pool.close()
pool.join()

print 'All subprocesses done.'
