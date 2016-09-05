#coding=utf8
import codecs
from lxml import etree
import os
import xlwt

def createExcel(setA,setB,now,last,path):
    book = xlwt.Workbook(encoding = 'utf-8',style_compression = 0)
    sheet = book.add_sheet('path',cell_overwrite_ok = True)

    # if (os.path.exists("/" + path)):
    #     os.mkdir("/" + path)
    #
    #     listA = setA & setB
    #     listB = setB - setA
    #     listC = setA - setB
    #
    #     for index in range(len(listA)):
    #         sheet.write(0, 0, "都有")
    #         sheet.write(index + 1, 0, str)
    #
    #     for index in range(len(listB)):
    #         sheet.write(0, 1, "本年无")
    #         sheet.write(index + 1, 1, str)
    #
    #     for index in range(len(listC)):
    #         sheet.write(0, 2, "前一年无")
    #         sheet.write(index + 1, 2, str)
    # else:
    #
    #
    #     listA = setA & setB
    #     listB = setB - setA
    #     listC = setA - setB
    #
    #
    #     for index in range(len(listA)):
    #
    #         sheet.write(0, 0, "都有")
    #         sheet.write(index + 1 ,0,str)
    #
    #     for index in range(len(listB)):
    #         sheet.write(0, 1, "本年无")
    #         sheet.write(index + 1, 1, str)
    #
    #     for index in range(len(listC)):
    #         sheet.write(0, 2, "前一年无")
    #         sheet.write(index + 1, 2, str)


    listA = setA & setB
    listB = setB - setA
    listC = setA - setB

    for index in range(len(listA)):
        sheet.write(0, 0, "都有")
        sheet.write(index + 1, 0, listA[index])

    for index in range(len(listB)):
        sheet.write(0, 1, "本年无")
        sheet.write(index + 1, 1, listB[index])

    for index in range(len(listC)):
        sheet.write(0, 2, "前一年无")
        sheet.write(index + 1, 2, listC[index])

    book.save(now + "-"+ last +".xls")

def read_xml(in_path):
    f = codecs.open(in_path,"r")
    content = f.read()
    f.close()
    tree = etree.parse(in_path)
    return tree

def countItem(path):
    for root, dirs, files in os.walk(os.path.abspath(path)):
        print root, dirs, files
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
                    if input.tag not in news_tags:
                        news_tags.append(input.tag)
                return set(news_tags)







def dealFile(path,list):

    realPath = path[2:]
    year = realPath.split('#')[0][:4]
    print list
    company_name =  realPath.split('#')[1]
    for str in list:
        if len(str) > 1:
            print str
            year1 = str[2:].split('#')[0][:4]
            company_name1 = str[2:].split('#')[1]
            if (company_name == company_name1 and int(year1) == int(year) - 1) :
                createExcel(countItem(path), countItem(str),year,year1, company_name)


if __name__ == "__main__":

    # find. - type d >> folder.txt
    file = open("/Users/liangxiansong/git4Madao/pythonCode/yinzhi/10KWork/GET/fold.txt")

    filePathlist = []
    while 1:
        line = file.readline()
        if not line:
            break
        else:
            filePathlist.append(line[:-1])
    file.close()

    for index in range(len(filePathlist)):
        try:
            dealFile(filePathlist[index], filePathlist)
        except Exception:
            print 'error : %s' % filePathlist[index]