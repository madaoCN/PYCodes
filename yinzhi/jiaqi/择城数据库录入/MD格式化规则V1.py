#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from SentenceModel import SententceModel
from MDError import MDError
import uuid
import MySQLdb as mdb
import pymongo
from MDSort import MDSort
from MDStack import Stack


LIST = []
config = {
    'host': '101.201.236.244',
    'port': 3306,
    'user': 'madao',
    'passwd': 'madao',
    'db': 'zeCheng',
    'charset': 'utf8'
}

conn = mdb.connect(**config)
#获取游标
cursor = conn.cursor()

FILE = codecs.open("/Users/liangxiansong/Desktop/result_out.txt", "a", "utf8")

stack_year = Stack()
stack_pl = Stack()
stack_po = Stack()
FLITERS = ["year", "month", "ns", "nt", "nposition"]

def mapItemsToList(item, stId):
    '''分割成list形式'''
    result = []
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
        result.append(stack_po.pop())
    while not stack_pl.empty():
        result.append(stack_pl.pop())
    while not stack_year.empty():
        result.append(stack_year.pop())


    result.reverse()
    # print " ".join(result)
    FILE.write( stId  + " " + " ".join(result)  +'\n')


# def main(stId):
#     sql = 'SELECT splitOrigSt FROM t_CaInfo WHERE stId = "%s"' % stId
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     for items in results:
#         for item in items:
#             mapItemsToList(item, stId)


def main(stIds):
    str = ''
    for item in stIds:
        str = str +  '"' + item  + '"' + ","

    sql = 'SELECT splitOrigSt, stId FROM t_CaInfo WHERE stId IN (%s)' % str.rstrip(',')
    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results)
    for items in results:
        mapItemsToList(items[0], items[1])

def LoadDB():
    idPath = os.path.join(os.path.expanduser("~"), "Desktop", 'stIDs.txt')
    with codecs.open(idPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            LIST.append(line)

    # print len(LIST)
    for idx in range(len(LIST) / 50 + 1):
        pre = idx * 50
        suf = (idx + 1) * 50
        if suf > len(LIST):
            main(LIST[pre:suf])
            print pre, len(LIST)
        else:
            main(LIST[pre:suf])
            print pre, suf


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

def removeTag(strline, replacement):
    '''
    去除标签
    :param strline:
    :return:
    '''
    result = re.sub('(/.+?\\b)', replacement, strline).replace(' ', '').rstrip('_')
    # str = '_'.join(result)
    # str = str.replace('/', '')
    return result

def write(tid, arr):
    orign = " ".join(arr)
    tagSet = praseTagSet(orign)
    wordSet = removeTag(orign, '_')
    # print orign
    # print tagSet
    # print wordSet
    print tid + "##" + orign + "##" + tagSet + "##" + wordSet
    FILE.write(tid + "##" + orign + "##" + tagSet + "##" + wordSet)
    FILE.write('\n')

def dealFormat():
    idPath = os.path.join(os.path.expanduser("~"), "Desktop", 'result.txt')
    with codecs.open(idPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            arr = line.split(' ')
            tid = arr[0]
            arr = arr[1:-1]
            write(tid, arr)




if __name__ == "__main__":
    LoadDB()

