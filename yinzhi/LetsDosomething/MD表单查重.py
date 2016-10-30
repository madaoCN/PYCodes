#coding=utf8
import codecs
import os
import pymongo
import re

if __name__ == "__main__":

    #已调整
    downLoaded = set()
    with codecs.open('/Users/liangxiansong/Desktop/folder.txt') as file:
        for line in file.readlines():
            billId = line.strip().lstrip('./').rstrip('.html')
            downLoaded.add(billId)
    print '已调整',len(downLoaded)

    #未调整
    allSet = set()
    filePath = '/Users/liangxiansong/Desktop/folderNew.txt'
    with codecs.open(filePath) as file:
        for line in file.readlines():
            line = line.strip()
            if re.search('-', line):
                sp = line.split('-')
                prefix = sp[0]
                suff = sp[-1]
                if re.search('\d+$', prefix) and re.search('\d+$', suff):
                    for idx in range(int(prefix), int(suff) + 1):
                        allSet.add(idx)
                else:
                    print '非纯数字', line
            else:
                allSet.add(line)
    print '未调整',len(allSet)

    #比较
    resultSet = allSet & downLoaded
    print '结果',len(resultSet)

    for i in allSet:
        if int(i) < 3700:
            print i
    #
    # filePath = '/Users/liangxiansong/Desktop/unDownload.txt'
    # file = codecs.open(filePath,'w+', encoding='utf8')
    # for record in resultSet:
    #     print '写入文件。。。。',  record
    #     file.write(record + '\n')


    # allSet = set()
    # filePath = '/Users/liangxiansong/Desktop/all.txt'
    # file = codecs.open(filePath,'w+', encoding='utf8')
    # for item in secCom.find():
    #     print item['cikNumber'],item['acceptanceDatetime']
    #     print 'add to allSet %s' % item['cikNumber']+'_'+item['acceptanceDatetime']
    #     allSet.add(item['cikNumber']+'_'+item['acceptanceDatetime'])
    #
    # print len(allSet)
    #
    #
    # for record in allSet:
    #     print '写入文件。。。。',  record
    #     file.write(record + '\n')

