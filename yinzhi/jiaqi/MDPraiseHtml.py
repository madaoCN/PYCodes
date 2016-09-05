#!/usr/bin/env python
#coding=utf8
import re
import codecs
import chardet
from bs4 import BeautifulSoup
import pprint
import pymongo


FILE = '/Users/liangxiansong/Desktop/test/test.html'
conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
PROVINCE = conn.zeCheng.province
LINKS = conn.zeCheng.link
def getArgs(file=FILE):
    '''
    获取题干或者答案的所有选择项
    :param file:文件路径
    :return:数据集合
    '''
    DIC = {}

    try:
        file = codecs.open(file, encoding='utf8')
        soup = BeautifulSoup(file.read(),'lxml')
        table = soup.find_all('table')[10]
        tds =  table.find_all('td',{'align':'left','valign':'top'})
        for td in tds:
            # aList = td.find_all('a')#省市区集合录入数据库  已完成
            # for a in aList:
            #     if not LINKS.find_one({'name':a.text}):
            #             LINKS.insert({'name':a.text , 'link': a['href']})
            for li in td.ul:
                cityList = []
                try:#省
                    province = li.a.text
                except Exception, e:
                    pass
                try:
                    for ul_li in li.ul:
                        try:
                            city = ul_li.a.text#市
                            areaList = []
                            try:
                                for areaTag in ul_li.ul:
                                    try:
                                        area = areaTag.a#区
                                        areaList.append(area.text)
                                    except Exception, e:
                                        pass

                            except Exception, e:
                                pass
                            cityList.append({city:areaList})
                        except Exception, e:
                            pass
                    print province
                    # DIC = {province:cityList}
                    # PROVINCE.insert(DIC)
                except Exception, e:
                    # if province == u'上海市' or province == u'天津市':
                    #     print '======='
                    #     print province
                    pass
    except Exception,e:
        print 'error !!!'
        print e


    return DIC

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(getArgs(FILE))