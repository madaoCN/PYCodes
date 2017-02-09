#coding=utf8
import xlrd, xlwt
import  xdrlib ,sys
import re
import chardet
import sys
import sys
import os
import xlrd
import chardet
from xlutils.copy import copy
import codecs
from bs4 import BeautifulSoup

reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

def writeExcelWithTable(tables, file= 'out.xls'):
    '''write something to excel file with table'''
    workBook = xlwt.Workbook()
    workSheet = workBook.add_sheet('sheet0')
    rownum = len(tables)
    for i in range(0,rownum-1):
        colnum = len(tables[i])
        rowlist = tables[i]
        for j in range(len(rowlist)):
            # print rowlist[j].decode('utf8')
            # print chardet.detect(rowlist[j])
            workSheet.write(i, j, rowlist[j].decode('utf8'))
    workBook.save(file)

def open_excel_xml(filename= 'file.xls'):
  try:
      if os.path.exists(filename):
          print 'file exist'
          # for item in xlrd.open_workbook(file).sheets():
          #     print item
          # print xlrd.open_workbook(file).sheet_by_index(0)
          with codecs.open(filename, 'r') as file:
              soup = BeautifulSoup(file, 'lxml')
              sheets = soup.find_all('worksheet')  # sheet集合
              return sheets
          # return xlrd.open_workbook(file)
      return None
  except Exception,e:
     print str(e)

def readdir(rootdir):
    #excel = r'...\merger1.xls'
    #rdx = open_excel('merger1.xls')
    #wtx = copy(rdx)  # 复制为可读写的wtx

    outsheet = []
    j = 1 # 为合并文件中的一行
    for parent, dirnames, filenames in os.walk(rootdir):
        print parent  # 查看文件的父目录
        for filename in filenames:  # 将文件夹下所有文件写入Excel，每个文件
            abspath = os.path.join(parent, filename)
            f = open(abspath, 'r')
            if os.path.basename(abspath).endswith('.xls'):
                sheets = open_excel_xml(abspath)  # 所有sheet
                table = sheets[0]
                rows = table.find_all('row')  # 按行(row)读取
                for rowidx in range(1,len(rows)-1):
                    outrow = ['', '', '']
                    outrow[0] = filename #文件名
                    inrows = rows[rowidx].find_all('cell')  # 源文件中的行
                    q = inrows[0].text #提问
                    a = inrows[1].text #回答
                    outrow[1] = q
                    outrow[2] = a
                    outsheet.append(outrow)
                    j += 1
    print("write new information successfully")
    writeExcelWithTable(outsheet, 'merger1.xls')
    print ("save the information successfully!")

def main():
    dataPath = os.path.join(os.path.expanduser('~'), 'Desktop', 'data')
    rootdir='data1/'
    rootdir = dataPath
    readdir(rootdir)
    s=0
    s=s+1

if __name__=="__main__":
    main()
