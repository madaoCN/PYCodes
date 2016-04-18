# coding=utf-8

import gzip
import urllib
from StringIO import StringIO
import base64
import codecs
import chardet
from Crypto.Cipher import AES


sting = 'v9kbOwPbm1uuDOClpYWnZWJvCSNiThP8ki6p1sDH6kmXNONRxWC7msywsyCKwoy0KHuypa9ZsCiu%0AWoTyeiThns2TTtP%2BPCw2YtpFIE77vGG6t3hlpQcGARVvsiWhsI0S%0A'
base =  urllib.unquote(sting)
print base

# base64解密
result = base64.b64decode(base)

dec = AES.new('doctorpda6666666', AES.MODE_CBC, b'doctorpda6666666')
plain = dec.decrypt(result)
print plain


#加密
data = '{"limit":20,"layer":"TwoLayer","id":"12497","order":"like_count","type":"community_topic","p":1}'
i = dec.block_size
j = len(data)
temp = j
if j % i != 0:
    j += i - j % i;
print j, temp


liang = dec.encrypt(data)
print base64.b64encode(liang)






