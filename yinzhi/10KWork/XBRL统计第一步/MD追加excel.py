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
            cik = table.cell(row, 0).value
            acceptanceDateTime = table.cell(row, 2).value[:4]
            print acceptanceDateTime, cik , row
            jsonDic = getItems(acceptanceDateTime, cik)

            idx = 13
            try:  # 公司名
                if jsonDic['companyName'] != None:
                    writeBook.get_sheet(0).write(row, idx, jsonDic['companyName'])
            except:
                pass
            # try:  # 公司ID
            #     if jsonDic['period'] != None:
            #         writeBook.get_sheet(0).write(row, idx + 1, jsonDic['period'])
            # except:
            #     pass
            writeBook.save(filePath)
        print '写入成功。。。'

def getItems(*key):
    # record = secCom.find_one({'acceptanceDatetime':{'$regex':key[0]}, 'cikNumber':key[1]})
    record = secCom.find_one({'cikNumber':key[1]})
    return record

if __name__ == '__main__':
    DIR = '/Users/liangxiansong/Desktop/resultcount_0.xls'
    addItems(DIR)



