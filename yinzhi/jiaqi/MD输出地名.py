#coding=utf8

import pymongo


mongoConn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
mongoCursor = mongoConn.zeCheng
provinceCollection = mongoCursor.province


try:
    locationDic = set()
    #读取mongo数据
    results = provinceCollection.find()
    idx = 1001
    for result in results:
        for key in result:
            if key != '_id':
                provinceName = key#获取到对应省名
                print provinceName
                locationDic.add(provinceName)
                #遍历市
                for cityDic in result[key]:
                    for city in cityDic:
                        cityName = city#获取到对应市名
                        print cityName
                        locationDic.add(cityName)
                        if cityDic[city]:
                            for distric in cityDic[city]:
                                print distric
                                locationDic.add(distric)

            # exit(0)
    print len(locationDic)
    import codecs
    import os
    filePath = os.path.join(os.path.expanduser('~'), 'Desktop', 'location.txt')
    with codecs.open(filePath, 'w+', encoding='utf8') as file:
        for item in locationDic:
            file.write(item)
            file.write('\n')
    file.close()


except Exception,e:
    print 'error'
    print e


