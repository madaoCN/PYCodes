#coding=utf8
import zlib
import chardet

s = r'''{\"device\":{\"platform\":\"android\",\"idfa\":\"e721e44d-ba72-3ec7-b90c-cd0d81bd8932\",\"macAddress\":\"9c:c1:72:6f:4d:59\",\"imei\":\"864036028378890\"},\"command\":\"message\\/notification\",\"user\":{\"uid\":\"302142\",\"nickname\":\"unicorn1369\",\"access_token\":\"y7NQT9BV8BB8F~nPdDjlf5ir7amkekGpjKpT7-QVn85sZ4FVertH-2w6EfgnPJIECwDGBGZbKqSAizFe\"},\"soft\":{\"coopId\":\"10020\",\"version\":\"2.1.4\",\"productId\":\"3001\"},\"request\":{\"user_id\":\"302142\"}}'''
print len(s)
print s.encode('utf8')
c = zlib.compress(s.encode('utf8'))

byteStr = bytearray(c)
for i in range(0, len(byteStr)):
    byteStr[i] = 0x5A ^ byteStr[i]
print byteStr








