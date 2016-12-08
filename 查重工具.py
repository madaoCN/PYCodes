#coding=utf8
import codecs
import os
import pymongo

if __name__ == "__main__":


    #svn远程
    remote = set()
    with codecs.open('/Users/liangxiansong/Desktop/test.txt') as file:
        for line in file.readlines():
            remote.add(line.strip())
    print 'svn远程',len(remote)

    #本地
    localFile = set()
    with codecs.open('/Users/liangxiansong/Desktop/svn.txt') as file:
        for line in file.readlines():
            localFile.add(line.strip())
    print 'svn本地', len(localFile)

    allSet =  localFile - remote
    for record in allSet:
        print record

    # #全集
    # allSet = set()
    # filePath = '/Users/liangxiansong/Desktop/XBRLDown/all.txt'
    # with codecs.open(filePath) as file:
    #     for line in file.readlines():
    #         dirNameList = line.split('_')
    #         if len(dirNameList) < 2:
    #             continue
    #         acceptTime = dirNameList[-1].strip()
    #         cik = os.path.basename(dirNameList[0])
    #         # print 'add to all Set %s' % cik+'_'+acceptTime
    #         allSet.add(cik+'_'+acceptTime)
    # print '全集',len(allSet)
    #
    # #比较
    # resultSet = allSet - downLoaded
    # print '结果',len(resultSet)
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


    # for record in allSet:
    #     print '写入文件。。。。',  record
    #     file.write(record + '\n')

