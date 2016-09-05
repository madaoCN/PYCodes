#coding=utf8
import requests
from requests import Session, Request
from multiprocessing import Pool,Process
import time
import re
import os
import urllib
import wget
BASE_URL = 'http://www.hotelaah.com/liren/index.html'

def downUrlRetrieve(dirName, url, fileName):
    '''
    下载URL
    '''
    print "downloading with requests"
    try:
        r = requests.get(url)
        fileDir = os.path.join(os.path.expanduser("~"), 'Desktop','test')
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
            print '创建目录。。', fileDir
        desktopPath = os.path.join(fileDir, fileName)
        print '-------------' + desktopPath
        print  time.strftime('%Y-%m-%d %X', time.localtime( time.time() ) )
        with open(desktopPath, "wb") as code:
            # code.write(MDCompressFile.gzip_compress(r.content))
            code.write(r.content)
    except Exception,e :
        print e
        print '出错了..'


if __name__ == "__main__":
    pool = Pool(5)
    pool.apply_async(downUrlRetrieve, args=('test', BASE_URL, 'test.html'))
    pool.close()
    pool.join()

