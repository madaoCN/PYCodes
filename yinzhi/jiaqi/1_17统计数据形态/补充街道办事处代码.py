#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
Citys = []
CityStr = ''
nsComplier = re.compile(u'(?<=[ ])[\u4e00-\u9fa5]+?(?=\/ns\\b)')


def loadFile(filePath):
    '''从文件路径 按行读取文件'''
    fileNameList = []
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            fileNameList.append(line)
    return fileNameList

if __name__ == "__main__":
    inputFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'nsCount.txt')
    citysFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'cityName.txt')
    Citys.extend(loadFile(citysFilePath))#读取区划
    with codecs.open(citysFilePath, 'r', 'utf8') as file:
        CityStr = file.read()

    outFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'out.txt')
    FILE = codecs.open(outFilePath, 'a', 'utf8')

    with codecs.open(inputFilePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            list = line.split("##")
            nullItem = list[2]
            city = list[1]
            sentence = list[-1]
            list = list[0:5]
            if nullItem == 'null':
                resultSet = set(re.findall('%s.' % city, CityStr))
                if len(resultSet) == 1:#若只有唯一
                    for item in resultSet:
                        list.append(item)
                        FILE.write('##'.join(list) + '\r\n')
                else:#存在多值情况
                    nsList = nsComplier.findall(sentence)
                    nsList = set(nsList)
                    nsList.remove(city)
                    if len(nsList):
                        ##(?<=(岳阳|安徽)).*?(桐城.).*?(?=(岳阳|安徽))
                        print '==========='
                        print city
                        # regexStr = u"(?<=[%s]).*?(%s.).*?(%s)*?" % ('|'.join(nsList), city,'|'.join(nsList))
                        regexStr = u"(?<=[%s]).*?(%s.)" % ('|'.join(nsList), city)
                        regexList = re.findall(regexStr, CityStr)
                        print regexStr
                        for item in set(regexList):
                            print item
                        # regexList = set(regexList)
                        # if len(regexList) == 1:
                        #     for item in regexList:
                        #         list.append(item)
                        #         FILE.write('##'.join(list) + '\r\n')
                # print city
                # for item in set(re.findall('%s.' % city, CityStr)):
                #     print item
                # print '========='