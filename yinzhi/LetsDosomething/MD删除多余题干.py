#coding=utf8
import pymongo
import os
from bs4 import BeautifulSoup
import re
import codecs
from bs4 import BeautifulSoup
import re



if __name__ == "__main__":
    # getTheRemoteAgent()
    # getLinkAndArea(os.path.join(os.path.expanduser('/'), 'Volumes', 'TOSHIBA EXT', 'baike'))
    allSet = set()
    def funx(args, dire ,files):
        for file in files:
            # if file.endswith('.html') and file.startswith('answer') :#获取要删除的文件名
            if file.endswith('.html'):#获取要删除的文件名
                target = os.path.join(dire, file)
                with codecs.open(target, encoding='utf8') as FILE:
                    fileContent = FILE.read()
                    result = re.search('document.title=.+?;', fileContent)
                    if result:
                        targetJsp = result.group(0).split(' ')[2]
                        print targetJsp
                        allSet.add(targetJsp)

                        targetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'result', targetJsp.replace(' ', '') + '.html')
                        print targetPath
                        file = codecs.open(targetPath, 'w+', encoding='utf8')
                        if file:
                            file.write(fileContent)
                            file.close()


    os.path.walk('/Users/liangxiansong/Desktop/财会分岗_data', funx, ())
    print len(allSet)
    # getLinkAndArea('/Users/liangxiansong/Desktop/会计恒等式.txt')