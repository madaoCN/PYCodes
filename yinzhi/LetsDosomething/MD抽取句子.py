#coding=utf8
import os
import codecs
import re
import pprint
from bs4 import BeautifulSoup
import shutil
from random import choice
from random import sample
from MDStack import Stack
import jieba

COUNT = 0

def breakSentencesByYear(sentence, FILE):
    '''
    按年份分词
    :param sentence:
    :return:
    '''
    print sentence
    FILE.write(sentence.strip())
    FILE.write('\r\n')
    return

    # 处理 \d{2}年 的情况
    for item in re.findall(u'\d{2}年', sentence):
        sentence = sentence.replace(item, item[:-1] + u'#')
    rowSen = sentence.strip().replace(u'——', u'#').replace(u'—', u'#')

    if not re.search('\d{2}', rowSen):
        return
    seg_list = jieba.cut(rowSen, HMM=True)
    # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    # 断句
    # divList = [li for li in seg_list]
    flag = 0
    mdStack = Stack()
    tempData = []
    tempStr = ''
    for li in seg_list:
        if li == ' ' and li == u'':
            pass
        if li != '#':
            mdStack.push(li)
        elif li == '#' and flag == 0:
            # mdStack.push('年')
            flag += 1
        elif li == "#" and flag > 0:
            temp = mdStack.pop()  # 抛出#号前一个
            while not mdStack.empty():
                tempData.append(mdStack.pop())
            tempData.reverse()
            writeContent = ''.join(tempData)
            print writeContent
            FILE.write(writeContent)
            FILE.write('\r\n')
            # paramDIC['sentence'].append(tempData)
            tempData = []
            mdStack.push(temp)
    tempData = []
    while not mdStack.empty():
        tempData.append(mdStack.pop())
    tempData.reverse()
    writeContent = ''.join(tempData)
    print writeContent
    FILE.write(writeContent)
    FILE.write('\r\n')

    # paramDIC['sentence'].append(tempData)

def findPersonalDetail(filePath, FILE):
    with codecs.open(filePath, encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        currentDir = os.path.dirname(filePath).split('/')[-1]
        print currentDir
        # divs = soup.find('div', {'class':'main-content'})
        currentTitle = ''
        flag = 0
        for div in soup.find('div', {'class':'main-content'}):
            # print '====='
            # print div
            try:
                if div.find('h2', {'class':'title-text'}):
                    print 'success---------'
                    contents = div.find('h2', {'class':'title-text'})
                    tag = contents.contents[-1]
                    if tag.encode('utf8') == currentDir:
                        flag = 1
                elif 'anchor-list' in div['class']:
                    # print div['class']
                    flag = 0
                elif flag == 1 and not 'para-title level-2' in div['class'] \
                        and div.name == 'div' and 'para' in div['label-module']\
                        and 'para' in div['class']:
                    divText = div.text.strip()
                    spliteEnd = re.split(u'。|;', divText)
                    # print spliteEnd

                    for end in spliteEnd:
                        end.strip(u' {}[],.（）\n\s').replace('\s', '')
                        if end != '' and end != ' ':
                            breakSentencesByYear(end, FILE)
            except Exception,e:
                pass

def funx(arg, dire, files):
    for file in files:
        if file.endswith('.txt'):
            print os.path.join(dire, file)
            jieba.load_userdict(os.path.join(dire, file))


if __name__ == "__main__":

    dicPath = os.path.join(os.path.expanduser('~'), 'Desktop', u'分词字典')
    os.path.walk(dicPath, funx, ())


    def funx(args, dire, files):
        # 文档集合文件
        FILE = codecs.open(dire+'/'+'sentences.txt', 'a', encoding='utf8')
        for file in files:
            currentFilePath = os.path.join(dire, file)
            # print '文件大小为 ',os.path.getsize(currentFilePath)
            if file.endswith('.html'):
                print '======当前文件是 ', currentFilePath
                findPersonalDetail(currentFilePath, FILE)
    os.path.walk('/Users/liangxiansong/Desktop/html', funx, ())