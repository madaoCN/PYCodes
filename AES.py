# coding=utf-8

import gzip
import urllib
from StringIO import StringIO
import base64
import codecs
from Crypto.Cipher import AES

string = 'fxQX4QJW33W3cUnL3RLBDq8AyxqOPlHaRy5dYClOqcKcGrRDqP8rP8NXrcG0tYnib2AWSxhrFi3ojLpWKSRe4oLC7bljldIOJ%2BLKOZHrQVp/x2nQrgb8kR5dDVmFl19B'
base =  urllib.unquote(string)
print base

# base64解密
result = base64.b64decode(base)

dec = AES.new('doctorpda6666666', AES.MODE_CBC, b'doctorpda6666666')
plain = dec.decrypt(result)
print plain


#加密
# data = '{"id":12492,"layer":"TwoLayer","type":"community_topic","p":1,"limit":10,"order":"like_count"}'
# i = dec.block_size
# j = len(data)
# temp = j
# if j % i != 0:
#     j += i - j % i;
# print j, temp
#
#
# liang = dec.encrypt(data + '0'*(j - temp))
# en = base64.b64encode(liang)
# print en







