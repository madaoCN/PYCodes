#coding=utf8
import os
import codecs
import re
import pprint
from bs4 import BeautifulSoup
COUNT = 0
resultDIC = {}
def findPersonalDetail(filePath):
    with codecs.open(filePath, encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        for title in soup.find_all('h2', {'class':'title-text'}):
            contents = title.contents
            if len(contents) == 2 and contents[0]['class'][0] == 'title-prefix':
                titleContent =  title.contents[-1]
                print titleContent
                if resultDIC.has_key(titleContent):#如果dic中已经存在字段
                    count = resultDIC[titleContent] + 1
                    resultDIC.update({titleContent:count})
                else:
                    resultDIC.update({titleContent: 1})
            else:
                print '==============='
                print contents

if __name__ == "__main__":
    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.html'):
                findPersonalDetail(os.path.join(dire, file))

    os.path.walk('/Users/liangxiansong/Desktop/baike/', funx,())
    print '写入文件。。。。。。。。'

    #写入文件
    targetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'titleRecord.txt')
    with codecs.open(targetPath, 'w+', encoding='utf8') as file:
        for key in resultDIC.keys():
            file.write(key+','+unicode(resultDIC[key]))
            file.write('\r\n')