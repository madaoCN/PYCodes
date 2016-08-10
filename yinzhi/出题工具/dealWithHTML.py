#!/usr/bin/env python
#coding=utf8
import re
import codecs
import chardet
import pprint

FILE = '/Users/lixiaorong/Desktop/jckj-data/6.2 利润表/利润表的编制实训（一）/利润表的编制1/answer-利润表的编制1.html'

def getArgs(file=FILE):
    '''
    获取题干或者答案的所有选择项
    :param file:文件路径
    :return:数据集合
    '''
    LIST = {}
    try:
        file = codecs.open(file, encoding='utf8')
        pattern = re.compile('var obj=document.getElementsByName.+obj.value=\'.+\';', re.I|re.M)
        list = pattern.findall(file.read())
        for item in list:
            try:
                # bTagPattern = re.compile('(\'.+\')')
                # bIndexPattern = re.compile('\[.+\]')
                tag = re.search('(\'.+?\')', item).group(0).strip('\'').strip()
                index = re.search('\[.+\]', item).group(0).strip()
                value = re.search('obj.value=.+\';', item).group(0).strip('obj.value=\';').strip()
                # print tag, index, value
                value = value.replace(',', '', )

                #假如匹配b (数组)
                if re.match('b', tag):
                    LIST[tag+str(index)] = value
                elif re.match('\w\d+', tag):
                    LIST[tag] = value
                else:
                    pass
                # LIST.append(item.split('\'')[1].encode('utf8'))
            except Exception, e:
                print e
                pass
    except Exception,e:
        print e


    return LIST

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(getArgs())