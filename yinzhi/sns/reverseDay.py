#coding=utf8
import time,datetime
import chardet
ISOFMT='%Y-%m-%d %X'

def getDate():
    curtf = datetime.datetime(*time.strptime(time.strftime("%Y-%m-5 00:00:00"), ISOFMT)[:6])
    for i in xrange(365*3):
        destf=curtf-datetime.timedelta(i)
        yield destf.strftime("%Y-%m-%d")
        # res.append(destf.strftime("%Y-%m-%d"))
        # if destf.day==25:#补加.day
        #     break
    # res.reverse()

def splitTimeStr(time):
    arr =  time.split('-')
    return arr[0]+'年'+arr[1]+'月'+arr[2]+'日'


# for item in getDate():
#     print str(item)
#     print splitTimeStr(item)
#     print chardet.detect(splitTimeStr(item))

