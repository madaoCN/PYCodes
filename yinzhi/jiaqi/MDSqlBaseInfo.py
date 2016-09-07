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
    if len(value) < 4:
        sql = 'INSERT INTO t_GovInfo  (id, province, city) values(%d,"%s","%s")' % value
    else:
        sql = 'INSERT INTO t_GovInfo values(%d,"%s","%s","%s")' % value
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
    TABLE_NAME = 't_BaseInfo'
    sql = 'CREATE TABLE %s' \
          '(id int primary key AUTO_INCREMENT,' \
          'name varchar(255) NOT NULL,' \
          'govID int NOT NULL DEFAULT 0,' \
          'primaryNative VARCHAR (255),' \
          'secondaryNative VARCHAR (255),' \
          'undergraduateSchool VARCHAR (255),' \
          'undergraduateMajor VARCHAR (255),' \
          'inDate VARCHAR (255),' \
          'outDate VARCHAR (255),' \
          'INDEX (govID),' \
          'CONSTRAINT fk_position FOREIGN KEY (govID) REFERENCES t_PositionInfo(govID))' % TABLE_NAME
    cursor.execute(sql)
    conn.commit()

    #读取mongo数据




except Exception,e:
    print 'error'
    print e


