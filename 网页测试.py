#coding=utf-8
import urllib
import urllib2
import re
import json, thread, threading,time,random
import os


# https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&query=李&filter={"clinic_no":"1"}&sort_type=default
string_1 = '''
https://api.chunyuyisheng.com/api/v4/doctor_search?page=5&query%3D%E7%BA%A2&filter%3D%7B%22clinic_no%22%3A%221%22%7D&sort_type=default&app=0&platform=android&systemVer=4.1.2&version=7.5.2&app_ver=7.5.2&imei=867746015013717&device_id=867746015013717&mac=c4%3A6a%3Ab7%3A53%3A24%3A1a&secureId=96a94c7b3102faac&installId=1454148004339&phoneType=MI+1S_by_Xiaomi&vendor=anzhihd

         '''
string_2 = '''
https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&query=%E6%9D%8E&filter=%7B%22clinic_no%22%3A%223%22%7D&sort_type=default&app=0&platform=android&systemVer=4.1.2&version=7.5.2&app_ver=7.5.2&imei=867746015013717&device_id=867746015013717&mac=c4%3A6a%3Ab7%3A53%3A24%3A1a&secureId=96a94c7b3102faac&installId=1454148004339&phoneType=MI+1S_by_Xiaomi&vendor=anzhihd

'''

# print urllib.quote()
print urllib.unquote(string_1)
print urllib.unquote(string_2)

time = [1,2,3,4,5,6,7]

def youCan():
    if len(time) == 7:
        print 'time == 7'
        return 0
        print 'next'












