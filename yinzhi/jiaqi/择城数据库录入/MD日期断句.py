# coding=utf8
import os
import codecs
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool

resultDIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'result')
delset = u'''\!"$%&'()\*\+,./:;<=>?@[\]\^_`{|}~;,。、；，：“”（）、？《》'''
# cp1 = re.compile(u'(?<=[%s自从于在当见间])(?P<year>19\d{2}|20\d{2})[年]' % delset)
# cp2 = re.compile(u'(?<=[\u4e00-\u9fa5])(19\d{2}|20\d{2})[年]')
cp1 = re.compile(u'(?<![至到-－-—-～－])(?P<year>19\d{2}|20\d{2})[年]')

def addTag(content):
    '''
    添加日期标志
    :param content:
    :return:
    '''
    content = cp1.sub(u'##\g<year>年', content)
    return content

def breakWords(dire, fileName):
    '''
    分词脚本
    :param dire:
    :param fileName:
    :return:
    '''
    # currentDIR = os.path.dirname(filePath)
    filePath = os.path.join(dire, fileName)#sentences文件地址
    resultFile = codecs.open(os.path.join(resultDIR, fileName),'w+', 'utf8')#目标存储文件地址
    with codecs.open(filePath, encoding='utf8') as file:
        sentenceList= []
        for line in file.readlines():
            line = line.strip()
            content = addTag(line)#添加日期标志
            sentenceList.extend(content.split('##'))
        for sentence in sentenceList:
            sentence = sentence.strip()
            if len(sentence)  > 3:
                resultFile.write(sentence + '\n')
def main(dire, file):
    try:
        # contetnt = getFileContent(os.path.join(dire, file))
        breakWords(dire, file)
    except Exception, e:
        print '**********' + file + '**********'
        print e


if __name__ == "__main__":
    if not os.path.exists(resultDIR):
        os.makedirs(resultDIR)

    pool = Pool(5)
    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.txt'):
                print file
                pool.apply_async(main, (dire, file))
                # main(dire, file)
    os.path.walk('/Users/liangxiansong/Desktop/sentences', funx, ())
    pool.close()
    pool.join()