#coding=utf8

import MySQLdb as mdb
import pymongo


config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'Lxs123456',
    'db': 'zeCheng',
    'charset': 'utf8'
}
conn = mdb.connect(**config)
#获取游标
cursor = conn.cursor()

mongoConn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
mongoCursor = mongoConn.zeCheng
provinceCollection = mongoCursor.province

def insertToDB(*value):
    #插入数据
    # value = (3, u'福建省', u'三明市', u'将乐县',)
    sql = None
    if len(value) == 2:
        sql = 'INSERT INTO t_GovInfo  (province, city) values("%s","%s")' % value
    else:
        sql = 'INSERT INTO t_GovInfo (province, city, district) values("%s","%s","%s")' % value
    print sql
    cursor.execute(sql)
    conn.commit()

try:
    # 创建数据库
    DB_NAME = 'zeCheng'
    # cursor.execute('DROP DATABASE IF EXISTS %s' % DB_NAME)
    cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)
    conn.commit()
    conn.select_db(DB_NAME)

    # 创建表
    TABLE_NAME = 't_GovInfo'
    # sql = 'CREATE TABLE %s' \
    #       '(id int primary key AUTO_INCREMENT,' \
    #       'province varchar(255) NOT NULL,' \
    #       'city VARCHAR (255),' \
    #       'district VARCHAR (255))' % TABLE_NAME
    # cursor.execute(sql)
    # conn.commit()

    #读取mongo数据
    results = provinceCollection.find()
    idx = 1001
    for result in results:
        for key in result:
            if key != '_id':
                provinceName = key#获取到对应省名
                sql = 'INSERT INTO t_GovInfo (province) values("%s")' % (provinceName, )
                print sql
                cursor.execute(sql)
                conn.commit()
                #遍历市
                for cityDic in result[key]:
                    for city in cityDic:
                        cityName = city#获取到对应市名
                        sql = 'INSERT INTO t_GovInfo  (province, city) values("%s","%s")' % (provinceName,cityName,)
                        print sql
                        cursor.execute(sql)
                        conn.commit()
                        if cityDic[city]:
                            for distric in cityDic[city]:
                                insertToDB(provinceName, cityName, distric)
                                print idx
                                idx += 1
                        else:
                            insertToDB(provinceName, cityName)
                            print idx
                            idx += 1
            # exit(0)



except Exception,e:
    print 'error'
    print e


