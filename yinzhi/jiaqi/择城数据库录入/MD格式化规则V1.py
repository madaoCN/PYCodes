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

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '',
    'db': 'zeCheng',
    'charset': 'utf8'
}

conn = mdb.connect(**config)
#获取游标
cursor = conn.cursor()

FILE = codecs.open("/Users/lixiaorong/Desktop/result.txt", "r", "utf8")

stack_year = Stack()
stack_pl = Stack()
stack_po = Stack()
FLITERS = ["year", "month", "ns", "nt", "nposition"]

def mapItemsToList(item):
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

    while not stack_year.empty():
        result.append(stack_year.pop())
    while not stack_pl.empty():
        result.append(stack_pl.pop())
    while not stack_po.empty():
        result.append(stack_po.pop())
    result.reverse()
    print result


def main(stId):
    sql = 'SELECT splitOrigSt FROM t_CaInfo WHERE stId = "%s"' % stId
    cursor.execute(sql)
    results = cursor.fetchall()
    for items in results:
        for item in items:
            mapItemsToList(item)



if __name__ == "__main__":
    idPath = os.path.join(os.path.expanduser("~"), "Desktop", 'stIDs.txt')
    with codecs.open(idPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            main(line)
