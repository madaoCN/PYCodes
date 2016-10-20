#!/usr/bin/env python
#coding=utf8
import dealWithHTML
import readDir
import os
import re
import pprint
import dealWithXML
import createXML
from bs4 import BeautifulSoup
import codecs


precision = 0.00001
class Spider:
    def __init__(self):
        self.currentDirName = ''
        self.dataDic = {}
        #variables 数据字典
        self.xmlData = {}
        #title 数据字典
        self.formData = {}
        #anser文件名
        self.answerFileName = ""
        #新增Tag
        self.moreTag = []

    def getDirFile(self, dir):
        '''
        获取目录下html文档路径
        :param dir: 路径
        :return: 文档路径集合
        '''
        fileList = []
        list = os.listdir(dir)
        if len(list) > 0:
            for file in list:
                filePath = os.path.join(dir, file)
                if not os.path.isdir(filePath):#如果是不是目录,是文件
                    fileList.append(filePath)

        return fileList

    def dealFilesWithPath(self, pathList):
        '''
        遍历文件,给出集合字典
        :return:
        '''
        fliterName = None
        index = 2
        if len(pathList) > 0:
            for file in pathList:

                #如果是xml文档
                if os.path.splitext(file)[-1] == '.xml':
                    #获取当前目录名称
                    currentDir = os.path.dirname(file).split('/')[-1]
                    #如果已经带有结果 则过滤
                    if not re.match(currentDir, os.path.basename(file)):
                        # print currentDir
                        # print os.path.basename(file)
                        # print '++++++++++++++++++++'
                        self.formData['T1'] = os.path.basename(file).rstrip('.xml')[1:].strip()
                        self.moreTag = dealWithXML.getVarible(file)
                    #T1改成文件名
                    # self.formData['T1'] = dealWithXML.getTitle(file)
                    # self.formData['T1'] = os.path.basename(file).rstrip('.xml')[1:].strip()
                    # self.moreTag = dealWithXML.getVarible(file)
                #如果是html文档
                elif os.path.splitext(file)[-1] == '.html':
                    #如果是anwser类型文件
                    fileName = os.path.split(file)[-1]
                    #判断文件名如果与'answer-'之后的重名则略过
                    # if fliterName and re.match(fliterName, fileName):
                    #     continue
                    args = dealWithHTML.getArgs(file)
                    if re.match(re.compile('\d?answer-'), fileName):
                        # fliterName = fileName.strip('answer-')
                        # print '过滤名', fliterName
                        self.dataDic['answer'] = args
                        self.answerFileName = fileName.rstrip('.html')[1:]
                    else:
                        if len(args) > 0:
                            self.dataDic['T' + str(index)] = args
                            self.formData['T' + str(index)] = fileName.rstrip('.html')[1:]
                            index += 1



    def matchTheSame(self, dic, key1, key2):
        '''

        :param list1:
        :param list2:
        :return:
        '''
        #判断是否为数字串
        pattern = re.compile(r'^[+-]?([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?$')
        for k1 in dic[key1]:
            for k2 in dic[key2]:
                value1 = dic[key1][k1]
                value2 = dic[key2][k2]
                #两者都是数字
                if pattern.match(value1) and pattern.match(value2):
                    try:
                        if abs(float(value1) - float(value2)) < precision:
                            # print '++++++++++++++++++++++++++'
                            # print key1 + '_' + k1, key2 + '_' + k2
                            # print value1, value2
                            #这里写插值函数
                            if isinstance(self.xmlData[key1 + '_' + k1], list):
                                self.xmlData[key1 + '_' + k1].append(key2 + '_' + k2)
                            elif self.xmlData[key1 + '_' + k1] == '##':
                                self.xmlData[key1 + '_' + k1] = key2 + '_' + k2
                            else:
                                tempList = []
                                tempList.append(self.xmlData[key1 + '_' + k1])
                                tempList.append(key2 + '_' + k2)
                                self.xmlData[key1 + '_' + k1] = tempList

                    except Exception, e:
                        print '====='
                        print value1, value2
                        print e
                        print '====='
                else:
                    if value1 == value2:
                        print '++++++++++++++++++++++++++'
                        print key1 +'_'+ k1, key2 + '_'+k2
                        print value1, value2
                        # 这里写插值函数
                        # 如果是list类型
                        if isinstance(self.xmlData[key1 + '_' + k1], list):
                            self.xmlData[key1 + '_' + k1].append(key2 + '_' + k2)
                        elif self.xmlData[key1 + '_' + k1] == '##':
                            self.xmlData[key1 + '_' + k1] = key2 + '_' + k2
                        else:
                            tempList = []
                            tempList.append(self.xmlData[key1 + '_' + k1])
                            tempList.append(key2 + '_' + k2)
                            self.xmlData[key1 + '_' + k1] = tempList

    def initXmlData(self):
        # keyNum = len(self.dataDic)
        # keyName = 'T'+str(keyNum)
        # try:
        #     dic = self.dataDic[keyName]
        #     for key in dic:
        #         print key
        #         self.xmlData[keyName+'_'+key] = "##"
        # except Exception, e:
        #     print e
        #     print 'error occur at initXmlData'
        dicNum = len(self.dataDic)
        for outKey in self.dataDic:
            for innerKey in self.dataDic[outKey]:
                if outKey == 'answer':
                    self.xmlData['T'+str(dicNum)+'_'+innerKey] = '##'
                else:
                    self.xmlData[outKey+'_'+innerKey] = '##'

    def main(self, path):
        #获取目录下的文件名
        filePathList = self.getDirFile(dir=path)

        self.dealFilesWithPath(filePathList)

        if len(self.dataDic) > 0:
            #将key由answer替换成T类型
            keyNum = len(self.dataDic) + 1
            try:
                self.dataDic['T'+str(keyNum)] = self.dataDic.pop('answer')
                self.formData['T'+str(keyNum)] = self.answerFileName
            except Exception, e:
                print e
            #修改key
            self.initXmlData()

            #匹配
            tempKey = []
            for key in self.dataDic:
                tempKey.append(key)
            tempKey.sort()

            if len(tempKey) > 1:
                for i in  range(len(tempKey)):
                    for j in range(i):
                        self.matchTheSame(self.dataDic, tempKey[i], tempKey[j])

            # for key in self.dataDic:
            #     if key != 'T'+str(keyNum):
            #         self.matchTheSame(self.dataDic,'T'+str(keyNum), key)

            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(self.xmlData)
            # return
            import sys
            reload(sys)
            sys.setdefaultencoding('utf-8')
            #写入xml
            doc = createXML.initalXML(self.formData, self.xmlData, self.moreTag)
            createXML.writeXML(path, doc)


if __name__ == '__main__':
    DIR = '/Users/liangxiansong/Desktop/test'

    def func(args,dire,fis):
        spider = Spider()
        spider.main(dire)

    os.path.walk(DIR, func, ())
    print 'process ============'