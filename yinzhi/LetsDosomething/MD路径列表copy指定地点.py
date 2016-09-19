#coding=utf8
import os
import codecs
import re
import pprint
from bs4 import BeautifulSoup
import shutil
from random import choice
from random import sample

COUNT = 0
titleDIC = {}
def findPersonalDetail(filePath):
    with codecs.open(filePath, encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        for title in soup.find_all('h2', {'class':'title-text'}):
            contents = title.contents
            if len(contents) == 2 and contents[0]['class'][0] == 'title-prefix':#获取到所有标签
                titleContent =  title.contents[-1]
                print titleContent
                if titleDIC.has_key(titleContent):#如果dic中已经存在字段
                    titleDIC[titleContent].append(filePath)
            else:
                print '==============='
                print contents

if __name__ == "__main__":

    targetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'titleCount.txt')
    with codecs.open(targetPath, 'r+', encoding='utf8') as file:
        for line in file.readlines():
            print '==========='
            title = line.split('	')[0]
            print title
            # titleLIST.append(title.strip())
            titleDIC.update({title.strip():[]})

    pprint.pprint(titleDIC)


    def funx(args, dire, files):
        for file in files:
            currentFilePath = os.path.join(dire, file)
            # print '文件大小为 ',os.path.getsize(currentFilePath)
            if file.endswith('.html') and os.path.getsize(currentFilePath) > 30000:
                print '======当前文件是 ', currentFilePath
                print '文件大小为 ', os.path.getsize(currentFilePath)
                findPersonalDetail(currentFilePath)
    os.path.walk('/Users/liangxiansong/Desktop/baike', funx, ())

    pprint.pprint(titleDIC)

    #写入文件
    targetPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'html')
    for key in titleDIC.keys():
        currentDir = os.path.join(targetPath, key)
        print '========当前文件夹', currentDir
        if not os.path.exists(currentDir):
            os.makedirs(currentDir)

        #拷贝文件
        if len(titleDIC[key]) > 50:
            sli = sample(titleDIC[key], 50)
        else:
            sli = titleDIC[key]
        for path in sli:
            print path, u'拷贝到'
            target = os.path.join(currentDir, os.path.basename(path).decode('utf8'))
            print target
            shutil.copy(path, target)
        # with codecs.open(targetPath, 'w+', encoding='utf8') as file:
        #     for key in resultDIC.keys():
        #         file.write(key+','+unicode(resultDIC[key]))
        #         file.write('\r\n')