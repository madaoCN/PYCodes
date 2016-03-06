# coding=utf-8
#导入pymysql的包
import pymysql
import subprocess
import pytesseract
import PIL

try:
    p = subprocess.Popen(['tesseract', 'test.png', 'result'],stdout=subprocess.PIPE,
                 stdin=subprocess.PIPE)
except Exception, e:
    print e
p.wait()
with open('result.txt', 'r') as f:
    print f.read()