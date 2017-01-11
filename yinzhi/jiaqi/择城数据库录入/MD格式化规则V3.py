#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from MDError import MDError
from MDSort import MDSort
from MDStack import Stack

stack_year = Stack()
stack_pl = Stack()
stack_po = Stack()

cpYear = re.compile('(?<![a-zA-Z])year')
cpMonth = re.compile('(?<![a-zA-Z])month')
cpNs = re.compile('(?<![a-zA-Z])ns$')
cpNt = re.compile('(?<![a-zA-Z])nt$')
cpPosition = re.compile('(?<![a-zA-Z])nposition$')

FILE = codecs.open("/Users/liangxiansong/Desktop/out.txt", "a", "utf8")
FILE1 = codecs.open("/Users/liangxiansong/Desktop/out1.txt", "a", "utf8")
maxYear = 0
maxNs = 0
maxNt = 0

def formatItem(result1, result2, result3):
    global maxYear, maxNs, maxNt
    if maxYear == 0:
        maxYear =  len(result1)
    if maxNs == 0:
        maxNs =  len(result2)
    if maxNt == 0:
        maxNt =  len(result3)
    maxYear = min(maxYear, len(result1))
    maxNs = min(maxNs, len(result2))
    maxNt = min(maxNt, len(result3))
    print maxYear, maxNs, maxNt


def formatYear(list):
    yearNum = 0#年的数目
    yearParm = ['NA/NA', 'NA/NA', 'NA/NA', 'NA/NA']
    for idx in range(len(list)):  # 处理年份
        yearValue = list[idx]
        for i in range(len(yearParm)):
            if i % 2 == 0 and cpYear.search(yearValue):  # 年
                yearNum = yearNum
                if yearParm[i] == 'NA/NA':
                    yearParm[i] = yearValue
                    break
            elif i % 2 == 1 and cpMonth.search(yearValue):  # 月
                if yearParm[i] == 'NA/NA' and yearNum == 0:
                    yearParm[i] = yearValue
                    break
                elif yearParm[i] == 'NA/NA' and yearNum != 0:# 若年出现次数不为0
                    if i / (len(list)- 1) == 0:
                        yearParm[i+2] = yearValue
                        break
                    elif i / (len(list)- 1) != 0:
                        yearParm[i] = yearValue
                        break

    return yearParm


def formatNs(list):
    nsParm = []
    for idx in range(4):#处理ns
        if idx  > len(list) - 1:
            nsParm.append('NA/NA')
        else:
            nsParm.append(list[idx])
    return nsParm

def formatNtPosition(list):
    stack_po.clear()
    resutlList = []
    for item in list:
        if not cpPosition.search(item): #nt
            stack_po.push(item)
        else:#nposition
            tempList = []
            tempList.append(item)
            while not stack_po.empty():
                tempList.append(stack_po.pop())
            tempList.reverse()
            resutlList.append(tempList)
    return resutlList

def mapItemsToList(item, stId):
    '''分割成list形式'''
    resultPo = []
    resultPl = []
    resultYear = []
    list = item.split(" ")
    stack_year.clear()
    stack_pl.clear()
    stack_po.clear()
    for item in list:
        temp = item.split("/")[-1]
        if temp in ["year", "month"]:
            stack_year.push(item)
        elif temp in ["ns"]:
            stack_pl.push(item)
        elif temp in ["nt", "nposition"]:
            stack_po.push(item)

    while not stack_po.empty():
        resultPo.append(stack_po.pop())
    while not stack_pl.empty():
        resultPl.append(stack_pl.pop())
    while not stack_year.empty():
        resultYear.append(stack_year.pop())

    resultYear.reverse()
    resultPl.reverse()
    resultPo.reverse()


    # str =  "##" + '##'.join(formatYear(resultYear))
    # str = str + "##" + '##'.join(formatNs(resultPl))
    # for item in formatNtPosition(resultPo):
    #     if len(item) > 0:
    #         str = str + "##" + ' '.join(item)
    # return str

    result = []
    result.extend(formatYear(resultYear))
    result.extend(formatNs(resultPl))
    for item in formatNtPosition(resultPo):
        if len(item) > 0:
            result.extend(item)
    # formatNs(resultPl)
    # formatNtPosition(resultPo)
    string =  "##".join(map(lambda m : m.split('/')[0] , result))
    string1 = "##".join(map(lambda m : m.split('/')[-1] , result))
    FILE.write(stId + '##' + string + '\n')
    FILE1.write(stId + '##' + string1 + '\n')
def loadFile():
    idPath = os.path.join(os.path.expanduser("~"), "Desktop", 'target.txt')
    with codecs.open(idPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            mapItemsToList(line.split("##")[6], line.split("##")[1])
            # string = mapItemsToList(line.split("##")[6], line.split("##")[1])
            # FILE.write(line + string + '\n')
if __name__ == "__main__":
    loadFile()
