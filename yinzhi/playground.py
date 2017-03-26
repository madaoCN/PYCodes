# coding=utf-8
import re
import os
import urllib, urllib2
from bs4 import BeautifulSoup
from requests import Request,Session
import codecs
def main():
    uri = 'http://www.tandfonline.com/doi/pdf/10.1162/016366003322596936'
    session = Session()

    headers = {
'Cache-Control': 'max-age=3600',
# 'Content-Disposition': 'inline; filename="Paradox and Contradiction in Organizations Introducing Two Articles on Paradox and Contradiction in Organizations.pdf"',
'Content-Type': 'application/pdf; charset=UTF-8',
'Date': 'Mon, 20 Feb 2017 05:12:09 GMT',
'Pragma':'',
'Server':'AtyponWS/7.1',
# 'Set-Cookie': 'JSESSIONID=aaaTZbsjVeElW9B3QF_Ov; domain=.www.tandfonline.com; path=/',
'Transfer-Encoding': 'chunked',
'X-Webstats-RespID': '8629d7f4219efceee839e0f03b706b58'

    }
    prepare = Request('GET', uri, headers=headers).prepare()
    with codecs.open('test.pdf', 'w+') as file:
        try:
            r = session.send(prepare)
            if r.status_code >= 200 and r.status_code < 300:
                file.write(r.content)
            else:
                return None
        except Exception, e:
            print e






if __name__ == "__main__":
    # main()
