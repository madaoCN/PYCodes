#coding=utf8
import jieba
import re
import os
import codecs
from bs4 import BeautifulSoup
import jieba.analyse
import pprint
from MDStack import Stack

#base
paramDIC = {}

def findNativePlaceAndSchool(soup):
    '''查找籍贯和毕业院校'''
    dtName = soup.find_all('dt', {'class': 'basicInfo-item name'})
    dtValue = soup.find_all('dd', {'class': 'basicInfo-item value'})

    if not len(dtName):#如果没有找到格式化的毕业院校和籍贯
        return None, None

    dtName = [dt.text for dt in dtName]
    dtValue = [dt.text for dt in dtValue]

    nativePlace = None
    graduateSchool = None

    for dt in dtName:
        native = re.search(u'出生地', dt)
        school = re.search(u'毕业', dt)
        if native:
            nativePlace = dtValue[dtName.index(dt)]
        if school:
            graduateSchool = dtValue[dtName.index(dt)]
    if nativePlace:
        nativePlace = '##'.join(jieba.cut(nativePlace.strip()))

    return nativePlace, graduateSchool

# def breakSentencesByYear(sentence):
#     '''
#     按年份分词
#     :param sentence:
#     :return:
#     '''
#     # 处理 \d{2}年 的情况
#     for item in re.findall(u'\d{2}年', sentence):
#         sentence = sentence.replace(item, item[:-1] + u'#')
#     for item in re.findall(u'\d{2}\.', sentence):
#         sentence = sentence.replace(item, item[:-1] + u'#')
#     for item in re.findall(u'\d{2}－', sentence):
#         sentence = sentence.replace(item, item[:-1] + u'#')
#     print sentence
#     # seg_list = jieba.cut(sentence.strip().replace(u'——', u'#').replace(u'—', u'#')\
#     #                      .replace(u'至',u'#'), HMM=True)
#     seg_list = jieba.cut(sentence.strip(), HMM=True)
#     # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#     # 断句
#     # divList = [li for li in seg_list]
#     flag = 0
#     mdStack = Stack()
#     tempData = []
#     tempStr = ''
#     for li in seg_list:
#         if li == ' ' and li == u'':
#             pass
#         if li != '#':
#             mdStack.push(li)
#         elif li == '#' and flag == 0:
#             flag += 1
#         elif li == "#" and flag > 1:
#             temp = mdStack.pop()  # 抛出#号前一个
#             while not mdStack.empty():
#                 tempData.append(mdStack.pop())
#             tempData.reverse()
#             paramDIC['sentence'].append(tempData)
#             tempData = []
#             mdStack.push(temp)
#
#     tempData = []
#     while not mdStack.empty():
#         tempData.append(mdStack.pop())
#     tempData.reverse()
#     paramDIC['sentence'].append(tempData)

def breakSentencesByYear(sentence):
    '''
    按年份分词
    :param sentence:
    :return:
    '''
    for item in re.findall(u'\d{2}年|\d{2}\.', sentence):
        sentence = sentence.replace(item, item[:-1] + u'#')
    # for c in sentence:
    #     if re.search(u'[\u2014]', c):
    #         print c
    # return

    seg_list = jieba.cut(sentence.strip(), HMM=True)
    # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

    flag = 0
    mdStack = Stack()
    tempData = []
    tempStr = ''
    for li in seg_list:
        if li == ' ' and li == u'':
            pass
        if li != '#' and flag == 0:
            mdStack.push(li)
        elif li == '#' and flag == 0:
            flag += 1
        elif li != '#' and flag == 1:
            #判断是否带有除 (年,月,日,至) 以外的中文字符 [\u4e00-\u9fa5]
            if re.search(u'[-至到\u2014]', li):
                flag = 0
            mdStack.push(li)
        elif li == "#" and flag > 0:
            flag == 0
            temp = mdStack.pop()  # 抛出#号前一个
            while not mdStack.empty():
                tempData.append(mdStack.pop())
            tempData.reverse()
            paramDIC['sentence'].append(tempData)
            tempData = []
            mdStack.push(temp)

    tempData = []
    while not mdStack.empty():
        tempData.append(mdStack.pop())
    tempData.reverse()
    paramDIC['sentence'].append(tempData)



def dealPersonInfo(info):
    if re.search(u'(,|\s).+?(校)?(大学)?(学院)?(系)?(专业)', info):
        print '找到匹配项'
        print info
        print '//'.join(jieba.cut(info.strip(), cut_all=False, HMM=True))

def praseHTML(filePath):
    paramDIC.update({'sentence':[]})
    with codecs.open(filePath, encoding='utf8') as file:
        soup = BeautifulSoup(file, 'lxml')

        #获取籍贯和毕业院校
        nativePlace, graduateSchool = findNativePlaceAndSchool(soup)
        paramDIC.update({'nativePlaces':[nativePlace], 'graduateSchools':[graduateSchool]})

        pprint.pprint(paramDIC)

        content = soup.find_all('div',{'class':'para'})
        for div in content:
            divList = []
            divText = div.text.strip()
            
            spliteEnd = re.split(u'。|;|；', divText)

            for end in spliteEnd:
                end.strip(u' {}[],.（）\n\s')
                if end != '' and end != ' ':
                    breakSentencesByYear(end)
                    # if re.search(u'学习|毕业|学历', end):
                    #     print end

                    # seg_list = jieba.cut(end.strip())
                    # content = jieba.analyse.textrank(end, topK=20, withWeight=False, allowPOS=('ns', 'n','nt', 't', 'tg'))
                    # print '========='
                    # print end
                    # for seg in seg_list:
                    #     if re.search('19\d{2}', seg) or re.search('20\d{2}', seg) or re.search(u'现任', seg):
                    #         print seg
                    # for tent in content:
                    #     print tent

        # pprint.pprint(paramDIC)
        for li in paramDIC['sentence']:
            print '========='
            print ''.join(li)
            # paramLIST.append(divText)


def funx(arg, dire, files):
    for file in files:
        if file.endswith('.txt'):
            print os.path.join(dire, file)
            jieba.load_userdict(os.path.join(dire, file))

if __name__ == "__main__":

    dicPath = os.path.join(os.path.expanduser('~'), 'Desktop', u'分词字典')
    os.path.walk(dicPath, funx, ())

    jieba.enable_parallel(4)#并行分词
    BASEPATH = os.path.join(os.path.expanduser('~'), 'Desktop', 'test.html')
    praseHTML(BASEPATH)
