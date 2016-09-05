#!/usr/bin/env python
#coding=utf8
import os
import pymongo
import xlwt, xlrd
from xlutils.copy import copy
from multiprocessing import Pool,Process

conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
secCom = conn.secCom.rssInfo


def addItems(filePath):
    if os.path.exists(filePath):
        readBook = xlrd.open_workbook(filePath)
        table = readBook.sheets()[0]
        rows = table.nrows
        cols = table.ncols
        # 文件名称
        fileID = None
        writeBook = copy(readBook)

        for row in range(rows):
            fileID = table.cell(row, 0).value
            print row
            print fileID
            jsonDic = getItems(fileID)

            idx = 7
            try:  # 公司名
                if jsonDic['companyName'] != None:
                    writeBook.get_sheet(0).write(row, idx, jsonDic['companyName'])
            except:
                pass
            try:  # 公司ID
                if jsonDic['cikNumber'] != None:
                    writeBook.get_sheet(0).write(row, idx + 1, jsonDic['cikNumber'])
            except:
                pass
            try:  # 会计期间
                if jsonDic['period'] != None:
                    writeBook.get_sheet(0).write(row, idx + 2, jsonDic['period'])
            except:
                pass
            try:  # 报送期间
                if jsonDic['acceptanceDatetime'] != None:
                    writeBook.get_sheet(0).write(row, idx + 3, jsonDic['acceptanceDatetime'])
            except:
                pass

        writeBook.save(filePath)
        print '写入成功。。。'

def getItems(key):
    record = secCom.find_one({'files.fileName':key})
    return record


if __name__ == '__main__':
    DIR = '/Users/liangxiansong/Desktop/resultcount.xls'
    addItems(DIR)



