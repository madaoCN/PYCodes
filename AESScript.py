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
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return self.ciphertext

    def mydecrypt(self,text):
        cryptor = AES.new(self.key,self.mode, self.IV)
        plain_text  = cryptor.decrypt(text)
        return plain_text
text = '''{"case_id":2369}'''
en = mycrypt()
entext = en.myencrypt(text)
entext_base64 = base64.b64encode(entext)
print entext_base64
print urllib.quote(entext_base64)
# #解密
# detext_base64 = base64.b64decode(entext_base64)
# detext = en.mydecrypt(detext_base64).rstrip()
# print detext


