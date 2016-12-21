#coding= utf8

import codecs
import os
import re

def fliter(sentence):
    '''
    处理市委
    '''
    delset = u'''\!"#$%&'()\*\+,-./:;<=>?@[\]\^_`{|}~;,。、'''
    sentence = re.sub(u'(?<![%s省市区县州洲])(?P<name>[省市区县州洲])(?P<suff>[委长])' % delset,
                      '\g<name>\g<name>\g<suff>', sentence)
    return sentence

def replaceItem(content):
    #。。委 长 替换
    content = fliter(content)
    # #连续四个数字替换为
    content = re.sub(u'(?!<[\d])(?P<year>19\d{2}|20\d{2})(?!年)', u'\g<year>年', content)
    # #前面不为数字, 四位数字XXXX后面为. 符号的年份
    content = re.sub(u'(?!<[\d])(?P<year>19\d{2}|20\d{2})(?=[.])', u'\g<year>年', content)
    # #13年“科研集团化-高校 补年份
    content = re.sub(u'(?<![\d])(?P<year>[01][0-6])(?=年)', u'20\g<year>', content)
    # 87年“科研集团化-高校 补年份
    content = re.sub(u'(?<![\d])(?P<year>[4-9]\d)(?=年)', u'19\g<year>', content)

    # #在1987.-—6和
    # content = re.sub(u'(?<=[.-—])(?P<month>[01]*\d)(?![月])', u'\g<month>月', content)
    # # #前面不为数字, 后面不为年 数字 和 月,的两位数字
    # content = re.sub(u'(?<![\d])(?P<month>[01]*?\d)(?![年月日\d.．])', u'\g<month>月', content)
    # #前面为年。., 后面不为月 日 年 和数字 的月份
    # content = re.sub(u'(?<=[年])(?P<month>[01]*?\d)(?![日月年\d])', u'\g<month>月', content)
    #前面年加一个标点
    # content = re.sub(u'(?<=[年，, .．\s\-\—]{2})(?P<month>[01]*?\d)(?![日月年\d])', u'\g<month>月', content)
    return content


def doSomething(resultPath, dirPath):

    with codecs.open(resultPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            if line.endswith(".txt") and not line.endswith("t.txt") and not line.endswith("r.txt"):
                print os.path.join(dirPath, line.lstrip('./'))
                with codecs.open(os.path.join(dirPath, line.lstrip('./')), 'r', 'utf8') as resultFile:
                    content = resultFile.read()
                    content = replaceItem(content)
                    with codecs.open(os.path.join(dirPath, line.lstrip('./')), 'w', 'utf8') as modifyFile:
                        modifyFile.write(content)


if __name__ == "__main__":

    resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences', 'result.txt')
    dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences')

    # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'result.txt')
    # dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test')

    doSomething(resultPath, dirPath)