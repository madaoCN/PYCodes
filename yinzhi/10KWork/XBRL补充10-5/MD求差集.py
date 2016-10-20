#coding=utf8
import codecs
import os
import pymongo

if __name__ == "__main__":
    # conn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
    # secCom = conn.secCom.rssInfo
    #已下载
    downLoaded = set()
    with codecs.open('/Users/liangxiansong/Desktop/folder.txt') as file:
        for line in file.readlines():
            record = line.strip()
            # print record
            downLoaded.add(record)
    print '已下载',len(downLoaded)

    #全集
    allSet = set()
    filePath = '/Users/liangxiansong/Desktop/CIKs.txt'
    with codecs.open(filePath) as file:
        for line in file.readlines():
            record = line.strip()
            # print record
            allSet.add(record)
    print '10k全集',len(allSet)

    munisSet = allSet - downLoaded
    print len(munisSet)

    # #比较
    # resultSet = allSet - downLoaded
    # print '结果',len(resultSet)
    #
    filePath = '/Users/liangxiansong/Desktop/unDownload.txt'
    file = codecs.open(filePath,'w+', encoding='utf8')
    for record in munisSet:
        print '写入文件。。。。',  record
        file.write(record + '\n')


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

