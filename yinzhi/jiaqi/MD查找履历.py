#coding=utf8
import os
import codecs
import re
COUNT = 0

def findPersonalDetail(filePath):
    with codecs.open(filePath, encoding='utf8') as file:
        content = file.read()
        if not re.search(u'人物生平', content) and not re.search(u'履历', content):
            global COUNT
            COUNT += 1
            print filePath
            print COUNT

if __name__ == "__main__":
    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.html'):
                findPersonalDetail(os.path.join(dire, file))

    os.path.walk('/Users/liangxiansong/Desktop/baike/', funx,())