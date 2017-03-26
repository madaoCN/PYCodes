#coding=utf8
import requests
from requests import Session, Request
import time
import re
import os
from bs4 import BeautifulSoup
import codecs
from bs4 import NavigableString
from collections import defaultdict
import xlwt
from xlwt import Workbook
from xlwt import Worksheet


BASE_URL = 'http://www.hotelaah.com/liren/index.html'

def get_html(targetUrl = BASE_URL):
    r = requests.get(targetUrl)
    print r.encoding
    return r.text

def prase_html(content):
    soup = BeautifulSoup(content, 'lxml')
    resutlDic = {}
    if soup:
        table = soup.find_all('table')[10]
        tds = table.find_all('td', {'align':'left', 'valign':"top"})
        idx = 0

        provinceDic = defaultdict(dict)
        for td in tds:
            P_C_A = td.ul
            for li in P_C_A:
                if not isinstance(li, NavigableString):
                    province = li.a.text #省会
                    provinceDic[province]
                    cityDic = defaultdict(list)
                    try:
                        if li.ul != None:
                            for li in li.ul: #市列表
                                if not isinstance(li, NavigableString):
                                    city = li.a.text #市
                                    cityDic[city]
                                    if li.ul != None:
                                        for li in li.ul:  #区列表
                                            if not isinstance(li, NavigableString):
                                                area = li.text
                                                cityDic[city].append(area)
                                    provinceDic[province] = cityDic
                    except Exception, e:
                        print e
                        print li
        return provinceDic

# def mapFunciton():



if __name__ == "__main__":
    # content = get_html()
    filePath = 'zeCheng.html'
    with codecs.open(filePath, 'r', 'utf8') as file:
        dic = prase_html(file.read())
        book = Workbook()
        sheet = book.add_sheet('sheets0', cell_overwrite_ok=True)
        row = 0
        for province, proDic in dic.items():
            if not len(proDic):
                sheet.write(row, 0, province)
                row = row + 1
                continue
            for city, areaList in proDic.items():
                if not len(areaList):
                    print '##'.join([province, city])
                    sheet.write(row, 0, province)
                    sheet.write(row, 1, city)
                    row = row + 1
                    continue
                for area in areaList:
                    print '##'.join([province, city, area])
                    sheet.write(row, 0, province)
                    sheet.write(row, 1, city)
                    sheet.write(row, 2, area)
                    row = row + 1
        book.save('file.xls')

