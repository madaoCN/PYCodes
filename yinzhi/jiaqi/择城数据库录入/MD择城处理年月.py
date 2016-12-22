#coding= utf8

import codecs
import os
import re
from multiprocessing import Pool

# #连续四个数字替换为
cp1 = re.compile(u'(?!<[\d])(?P<year>19\d{2}|20\d{2})(?!年)')
# #前面不为数字, 四位数字XXXX后面为. 符号的年份
cp2 = re.compile(u'(?!<[\d])(?P<year>19\d{2}|20\d{2})(?=[.])')
# #13年“科研集团化-高校 补年份
cp3 = re.compile(u'(?<![\d])(?P<year>[01][0-9])(?=年)')
# 87年“科研集团化-高校 补年份
cp4 = re.compile(u'(?<![\d])(?P<year>[4-9]\d)(?=年)')
# 前面年加一个标点
cp5 = re.compile(u'(?<=年)(?P<month>[01]*?\d)(?![日月年\d])')
cp6 = re.compile(u'(?<=[年，, 。.．\s\-\— ]{2})(?P<month>[01]*?\d)(?![日月年\d])')

def fliter(sentence):
    '''
    处理市委
    '''
    delset = u'''\!"#$%&'()\*\+,-./:;<=>?@[\]\^_`{|}~;,。、'''
    sentence = re.sub(u'(?<![%s省市区县州洲])(?P<name>[省市区县州洲])(?P<suff>[委长])' % delset,
                      '\g<name>\g<name>\g<suff>', sentence)
    return sentence

def replaceItem(content):
    # #。。委 长 替换
    content = fliter(content)
    content = cp1.sub(u'\g<year>年', content)
    content = cp2.sub(u'\g<year>年', content)
    content = cp3.sub(u'20\g<year>', content)
    content = cp4.sub(u'19\g<year>', content)
    content = cp5.sub(u'\g<month>月', content)
    content = cp6.sub(u'\g<month>月', content)

    return content


def doSomething(dirPath, filePath):

    # with codecs.open(resultPath, 'r', 'utf8') as file:
    #     for line in file.readlines():
    #         line = line.strip()
    try:
        if filePath.endswith(".txt"):
            print os.path.join(dirPath, filePath)
            with codecs.open(os.path.join(dirPath, filePath), 'r', 'utf8') as resultFile:
                lines = []
                for line in resultFile.readlines():
                    line = line.strip()
                    line = replaceItem(line)
                    lines.append(line)

                with codecs.open(os.path.join(dirPath, filePath), 'w', 'utf8') as modifyFile:
                    for line in lines:
                        modifyFile.write(line + '\n')
    except Exception, e:
        print '*********' + filePath + '*********'
        print e

if __name__ == "__main__":

    # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences', 'folder.txt')
    # dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences')
    # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'result.txt')
    # dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test')

    pool = Pool(5)
    def funx(args, dire, files):
        for file in files:
            if file.endswith('.txt'):
                pool.apply_async(doSomething, (dire, file))
                # main(dire, file)

    os.path.walk('/Users/liangxiansong/Desktop/sentences', funx, ())
    pool.close()
    pool.join()
