#!/usr/bin/env python
#coding=utf8
from Crypto.Cipher import AES
import base64
import urllib
class mycrypt():
    def __init__(self):
        self.key = 'doctorpda6666666'
        self.mode = AES.MODE_CBC
        self.IV = 'doctorpda6666666'

    def myencrypt(self,text):
        cryptor = AES.new(self.key,self.mode, self.IV)
        length = AES.block_size
        count = text.count('')
        if count < length:
            add = (length-count) + 1
            text = text + (' ' * add)
        elif count > length:
            add = (length-(count % length)) + 1
            text = text + (' ' * add)
        self.ciphertext = cryptor.encrypt(text)
        return self.ciphertext

    def mydecrypt(self,text):
        cryptor = AES.new(self.key,self.mode, self.IV)
        plain_text  = cryptor.decrypt(text)
        return plain_text
text = '''{"limit":20,"layer":"TwoLayer","id":"12497","order":"like_count","type":"community_topic","p":1}'''
en = mycrypt()
entext = en.myencrypt(text)
entext_base64 = base64.b64encode(entext)
print entext_base64
print urllib.quote(entext_base64)
detext_base64 = base64.b64decode(entext_base64)
detext = en.mydecrypt(detext_base64).rstrip()
print detext

#真base64
lens = len(strg)
lenx = lens - (lens % 4 if lens % 4 else 4)
try:
    result = base64.decodestring(strg[:lenx])
    detext = en.mydecrypt(result).rstrip()
    print detext
except:
  pass
