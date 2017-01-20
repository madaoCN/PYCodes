#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from MDError import MDError
from MDNewFixModel import NewFixModel
from MDSort import MDSort
#预编译
cpYear = re.compile('(?<![a-zA-Z])year')
cpCountYear = re.compile('(?<![a-zA-Z])year')
cpCountNt = re.compile('(?<![a-zA-Z])nt(?![a-zA-Z])')
cpCountPosition = re.compile('(?<![a-zA-Z])nposition')
MDSortter = MDSort()

def praseTagSet(strline):
    '''
    抓取分词标签
    :param strline:
    :return:
    '''
    # list = strline.split(' ')
    # result = []
    # print strline
    # for item in list:
    #     temp = re.search('(?<=[/])(\w+)', item)
    #     result.append(temp.group(0))
    result = re.findall('(?<=[/])(\w+?)(?=[\s\b])', strline + ' ')
    str = '_'.join(result)
    # str = str.replace('/', '').rstrip('_')
    return str

def removeTag(strline, replacement = '_'):
    '''
    去除标签
    :param strline:
    :return:
    '''
    result = re.sub('(/.+?\\b)', replacement, strline).replace(' ', '').rstrip('_')
    # str = '_'.join(result)
    # str = str.replace('/', '')
    return result

def judgeYear(str):
    '''
    判断是带有年份
    :param str:
    '''
    return 'false' if cpYear.search(str) == None else 'true'

def countYear(string):
    '''判断year的数目'''
    return len(cpCountYear.findall(string))

def countNt(string):
    '''判断nt的数目'''
    return len(cpCountNt.findall(string))

def countnPosition(string):
    '''判断nt的数目'''
    return len(cpCountPosition.findall(string))


def main():
    targetFile = os.path.join(os.path.expanduser('~'), 'Desktop', 'out.txt')
    outFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', 'result.txt')
    FILE = codecs.open(outFilePath, 'a', 'utf8')
    with codecs.open(targetFile, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            list = line.split('##')
            splitedTag = praseTagSet(list[6]) #分词后tag集合
            splitedText = removeTag(list[6]) #分词后文本集合
            hasYear = judgeYear(splitedTag) #是否带有年份
            list = splitedTag.split('_')
            sortedTag = '_'.join(MDSortter.sortTag(list)) #tag排序
            yearNum = countYear(splitedTag)
            ntNum = countNt(splitedTag)
            npostionNum = countnPosition(splitedTag)
            FILE.write(line +'##' + '##'.join([splitedTag, splitedText,
                                         hasYear,
                                         sortedTag, str(yearNum),
                                         str(ntNum), str(npostionNum)]))
            FILE.write('\n')




if __name__ == "__main__":
    main()