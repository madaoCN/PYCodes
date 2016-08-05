#coding=utf-8
import os
import pymongo
import re
import xlwt

conn = pymongo.MongoClient("127.0.0.1", 27017, connect=False)
path = os.path.join(os.path.expanduser("~"), 'Desktop')




workBook1 = xlwt.Workbook()
workBook2 = xlwt.Workbook()
workBook3 = xlwt.Workbook()
sheet1 = workBook1.add_sheet('sns_1', cell_overwrite_ok=True)
sheet2 = workBook2.add_sheet('sns_2', cell_overwrite_ok=True)
sheet3 = workBook3.add_sheet('sns_3', cell_overwrite_ok=True)

# sheet = workBook.add_sheet('sns')
title = [u'提问人',u'提问时间',u'提问内容',u'上市公司',u'上市公司代码',u'上市公司回答内容',u'上市公司回答时间']
#写入头
def writeHead(head):
    index = 0
    for til in title:
        head.write(0, index, til)
        index += 1

writeHead(sheet1)
writeHead(sheet2)
writeHead(sheet3)

data = conn.test.DATA.find()
sheet = sheet1
row = 1
tag = 0
for item in data:
    print item
    sheet.write(row, 1, item['answerTime'])
    # 提问内容
    sheet.write(row, 2, item['askContent'])
    # 上市公司
    sheet.write(row, 3, item['answerMan'])
    # 上市公司代码
    sheet.write(row, 4, item['answerID'])
    # 上市公司回答
    sheet.write(row, 5, item['answerContent'])
    # 上市公司回答时间
    sheet.write(row, 6, item['answerTime'])
    try:
        # 提问人
        sheet.write(row, 0, item['askMan'])
        #提问时间
        print 'write at row: %s' % (row, )
    except Exception, e:
        print e
    finally:

        row += 1
        if row == 60000:
            tag = 2
            row = 1
        if row == 120000:
            tag = 3
            row = 1
        if tag == 2:
            sheet = sheet2
        if tag == 3:
            sheet = sheet3



workBook1.save('sns_1.xls')
workBook2.save('sns_2.xls')
workBook3.save('sns_3.xls')

print 'process completed'
