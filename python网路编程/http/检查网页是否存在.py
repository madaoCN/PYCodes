#coding=utf-8
#!/usr/bin/env python

import argparse
import httplib
import urlparse
import re
import urllib

DEFAULT_URL = 'http://www.python.org'
HTTP_Good_Codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]

def get_server_status_code(url):
    # 获取状态字
    host, path = urlparse.urlparse(url)[1:3]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None

if __name__ == "__main__":
    praser = argparse.ArgumentParser(description='nothing')
    praser.add_argument('--url', action='store', dest='url', default=DEFAULT_URL)
    given_args = praser.parse_args()
    url = given_args.url
    if get_server_status_code(url) in HTTP_Good_Codes:
        print 'server %s status is OK' % %url
    else:
        print 'server %s status is Not OK' % % url
