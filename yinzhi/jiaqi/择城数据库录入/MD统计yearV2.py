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
TOTAL_NUM = 166310
FILE = codecs.open("/Users/liangxiansong/Desktop/result_out.txt", "a", "utf8")
cpYear = re.compile('(?<![a-zA-Z])year')
cpNt = re.compile('(?<![a-zA-Z])nt(?=[_])')
cpPosition = re.compile('(?<![a-zA-Z])nposition(?=[_])')

def judgeYear(str):
    '''
    判断是带有年份
    :param str:
    :return:
    '''
    return 'true' if cpYear.search(str) == None else 'false'

def countYear(string):
    '''判断year的数目'''
    return len(cpYear.findall(string))

def countNt(string):
    '''判断nt的数目'''
    return len(cpNt.findall(string))

def countnPosition(string):
    '''判断nt的数目'''
    return len(cpPosition.findall(string))

def selectSQL(pre,suf):
    sql = 'SELECT stId, sortedTag from t_CaInfo LIMIT %s, %s' % (pre, suf)
    cursor.execute(sql)
    results = cursor.fetchall()

    insertSql = 'UPDATE t_CaInfo set hasYear=CASE stId' \
                '%s'\
                ' END, ' \
                'yearNum=CASE stId' \
                '%s' \
                ' END, ' \
                'ntNum=CASE stId ' \
                '%s' \
                ' END, ' \
                'npositionNum=CASE stId' \
                '%s' \
                ' END' \
                ' WHERE stId IN (%s)'
    hasYearPara = ''
    yearNumPara = ''
    ntNumPara = ''
    npositionNumPara = ''
    stIdPara = []
    for items in results:
        stId = items[0]
        tagSet = items[1]
        hasYear = judgeYear(tagSet)
        yearCount = countYear(tagSet)
        ntCount = countNt(tagSet)
        positionCount = countnPosition(tagSet)

        hasYearPara = hasYearPara + ' WHEN "%s" THEN "%s"' % (stId, hasYear)
        yearNumPara = yearNumPara + ' WHEN "%s" THEN "%s"' % (stId, yearCount)
        ntNumPara = ntNumPara + ' WHEN "%s" THEN "%s"' % (stId, ntCount)
        npositionNumPara = npositionNumPara + ' WHEN "%s" THEN "%s"' % (stId, positionCount)
        stIdPara.append(stId)
        # print yearCount, ntCount, positionCount

    # print insertSql % (hasYearPara, yearNumPara, ntNumPara, npositionNumPara, '"' + '","'.join(stIdPara) + '"')
    cursor.execute(insertSql % (hasYearPara, yearNumPara, ntNumPara, npositionNumPara, '"' + '","'.join(stIdPara) + '"'))
    conn.commit()

def main():
    idPath = os.path.join(os.path.expanduser("~"), "Desktop", '12-23data.txt')
    with codecs.open(idPath, 'r', 'utf8') as file:
        for line in file.readlines():
            try:
                line = line.strip()
                list = line.split("\t")
                id = list[0]  # id
                stID = list[1]  # 句子ID
                hmName = list[2]  # 人名
                hmId = list[3]  # 人ID
                fileName = list[4]
                originSt = list[5]  # 原始句子
                splitSt = list[6]  # 分词后句子
                tagSet = list[7]  # 标签集合
                removeTagSt = list[8]  # 去除标签集合
                hasYear = list[9]  # 是否含年份
                sortedTagSet = list[10]  # 排序后tag
                # print len(list)

            except Exception, e:
                # print len(list)
                # print line
                if len(list) < 11:
                    result = line.replace("#", '\t')
                    list = result.split("\t")
                    id = list[0]  # id
                    stID = list[1]  # 句子ID
                    hmName = list[2]  # 人名
                    hmId = list[3]  # 人ID
                    fileName = list[4]
                    originSt = list[5]  # 原始句子
                    splitSt = list[6]  # 分词后句子
                    tagSet = list[7]  # 标签集合
                    removeTagSt = list[8]  # 去除标签集合
                    hasYear = list[9]  # 是否含年份
                    sortedTagSet = list[10]  # 排序后tag
            finally:
                yearNum = countYear(sortedTagSet)
                ntNum = countNt(sortedTagSet)
                ptNum = countnPosition(sortedTagSet)
                string = "##".join([str(id), stID, hmName, str(hmId),
                                    fileName, originSt, splitSt, tagSet,
                                    removeTagSt, hasYear, sortedTagSet, str(yearNum),
                                    str(ntNum), str(ptNum)])
                FILE.write(string +'\n')

    # selectSQLidx

if __name__ == "__main__":
    main()