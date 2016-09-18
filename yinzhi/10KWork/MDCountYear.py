#!/usr/bin/env python
#coding=utf8
import codecs
from lxml import etree
import os
import xlwt
import glob

IDX = 0
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('path', cell_overwrite_ok=True)

def createExcel(company_name, setA,setB,now,last, index):


    listA = setA & setB
    listB = setB - setA
    listC = setA - setB

    print company_name, now+'-'+last, len(listA), len(listB), len(listC)
    global IDX
    IDX += 1
    sheet.write(index, 0, company_name)
    sheet.write(index, 1, now)
    sheet.write(index, 2, last)
    sheet.write(index, 3, len(listA))
    sheet.write(index, 4, len(listB))
    sheet.write(index, 5, len(listC))


def read_xml(in_path):
    f = codecs.open(in_path,"r")
    content = f.read()
    f.close()
    tree = etree.parse(in_path)
    return tree

def countItem(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("_base.xml"):
                pass

            elif file.endswith("_ext.xml"):
                pass
            elif file.endswith(".xml"):

                tree = read_xml(path+"/"+file)
                inputs = tree.getroot().xpath("//*")

                news_tags = []

                for input in inputs:
                    inputTag = input.tag.split('}')[-1]
                    if inputTag not in news_tags:
                        news_tags.append(inputTag)
                return set(news_tags)

def deal(path, forPath):
    realPath = path[2:]
    year = realPath.split('#')[0][:4]
    company_name = realPath.split('#')[1]
    year1 = forPath[2:].split('#')[0][:4]

    try:
        createExcel(company_name, countItem(path), countItem(forPath), year, year1, IDX)
    except Exception, e:
        print '======'
        print path
        print e


def dealFile(path,list):
    realPath = path[2:]
    year = realPath.split('#')[0][:4]
    company_name =  realPath.split('#')[1]

    for str in list:
        if len(str) > 1:
            year1 = str[2:].split('#')[0][:4]
            company_name1 = str[2:].split('#')[1]
            if (company_name == company_name1 and int(year1) == int(year) - 1) :
                global IDX
                IDX += 1
                createExcel(company_name,countItem(path), countItem(str),year,year1,IDX)

    book.save("countYear.xls")


if __name__ == "__main__":

    # find. - type d >> folder.txt
    file = open("folder.txt")

    filePathlist = []
    while 1:
        line = file.readline()
        if not line:
            break
        else:
            print '==='
            print line
            print line[:-1]
            filePathlist.append(line[:-1])
    file.close()

    for index in range(len(filePathlist)):
        # if index > 5:
        #     continue
        try:
            list = filePathlist[index].split('#')
            if len(list) > 1:
                year =  list[0][-8:-4]
                forYear = int(year) -1
                for f in glob.iglob(r'./%s*#%s' % (forYear, list[-1])):
                    deal(filePathlist[index], f)
            # # dealFile(filePathlist[index], filePathlist)
            book.save("countYear.xls")
        except Exception, e:
            print e
            print 'error : %s' % filePathlist[index]
