#coding=utf8
import re

import MySQLdb as mdb

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
# FILE = codecs.open("/Users/liangxiansong/Desktop/result_out.txt", "a", "utf8")
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
    for idx in range(TOTAL_NUM /100 + 1):
        pre = idx * 100
        suf = (idx + 1) * 100
        if suf > TOTAL_NUM:
            print pre, TOTAL_NUM
            selectSQL(pre, TOTAL_NUM)
        else:
            print pre, suf
            selectSQL(pre, suf)

    # selectSQLidx

if __name__ == "__main__":
    main()