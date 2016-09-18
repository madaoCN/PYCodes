#coding=utf8
import pymongo
import os
from bs4 import BeautifulSoup
import re
import codecs


def getLinkAndArea(filePath, targetPath,offset):

    print targetPath
    targetFile = codecs.open(targetPath, 'w+', encoding='utf8')
    with codecs.open(filePath, encoding='utf8') as file:
        for line in file.readlines():
            line = line.strip()
            result = re.findall(':\d{2}', line)
            if len(result) == 2:
                minute = result[0]
                second = result[1]
                currentTime = int(minute.strip(' :')) * 60 + int(second.strip(' :'))
                currentTime -= int(offset)

                minute = currentTime / 60
                second = currentTime % 60

                if minute < 10:
                    minute = '0%d' % minute
                else:
                    minute = '%d' % minute

                if second < 10:
                    second = '0%d' % second
                else:
                    second = '%d' % second

                # print '00:%s:%s' % (minute, second,)
                prefix = '00:%s:%s###' % (minute, second,)
                # print line.replace('\d{2}:\d{2}:\d{2}', '00:%s:%s' % (minute, second,))
                content = line.split('###')
                content = prefix + content[-1]
                targetFile.write(content)
                targetFile.write('\n')
            elif len(result) == 3:
                minute = result[0]
                second = result[1]
                microSec = result[2]
                currentTime = int(minute.strip(' :')) * 60 + int(second.strip(' :'))
                currentTime -= int(offset)

                minute = currentTime / 60
                second = currentTime % 60

                if minute < 10:
                    minute = '0%d' % minute
                else:
                    minute = '%d' % minute

                if second < 10:
                    second = '0%d' % second
                else:
                    second = '%d' % second

                # print '00:%s:%s' % (minute, second,)
                prefix = '00:%s:%s%s###' % (minute, second, microSec)
                # print line.replace('\d{2}:\d{2}:\d{2}', '00:%s:%s' % (minute, second,))
                content = line.split('###')
                content = prefix + content[-1]
                targetFile.write(content)
                targetFile.write('\n')


if __name__ == "__main__":
    # getTheRemoteAgent()
    # getLinkAndArea(os.path.join(os.path.expanduser('/'), 'Volumes', 'TOSHIBA EXT', 'baike'))
    targetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'ZMResult')
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.txt'):
                offset = re.search('(\d+)', file).group(0)
                getLinkAndArea(dire + '/' +file, os.path.join(targetPath, file),offset)


    os.path.walk('/Users/liangxiansong/Desktop/字幕搜索', funx, ())
    # getLinkAndArea('/Users/liangxiansong/Desktop/会计恒等式.txt')