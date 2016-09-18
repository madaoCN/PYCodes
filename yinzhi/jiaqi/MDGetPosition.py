#coding=utf8

import MySQLdb as mdb
import MDPraseDetail
import pymongo
#BASE
#MONGODB
mongoConn = pymongo.MongoClient("202.120.24.213", 27017, connect=False)
mongoCursor = mongoConn.zeCheng
provinceCol = mongoCursor.province
linkCol = mongoCursor.link
#MYSQL
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
cursor = conn.cursor(cursorclass=mdb.cursors.DictCursor)

def getSql(tableName ,name):

    sql = None
    if name.endswith(u'省'):
        sql = '''SELECT * FROM %s WHERE province LIKE "%%%s%%"
                           ''' % (tableName, name,)
    elif name.endswith(u'市'):
        sql = '''SELECT * FROM %s WHERE city LIKE "%%%s%%"
                                   ''' % (tableName, name,)
    elif name.endswith(u'区') or name.endswith(u'县'):
        sql = '''SELECT * FROM %s WHERE district LIKE "%%%s%%"
                                   ''' % (tableName, name,)
    print name
    print sql

def insertSQL(value):
    sql = '''INSERT INTO t_PositionInfo (name,govID,
                                    provinceControl,cityControl,
                                    districtControl,position,
                                    startDate,endDate)
                                    values("%s",%d,
                                    "%s","%s",
                                    "%s","%s",
                                    "%s","%s")''' % value
    print sql
    cursor.execute(sql)
    conn.commit()
    print '插入数据库成功...........'

def getLinkAndArea():
    for item in linkCol.find():
        name = item['name']
        TABLE_NAME = 't_GovInfo'
        # getSql(TABLE_NAME, name)
        sql = '''SELECT * FROM %s WHERE province LIKE "%%%s%%"
                               OR city LIKE "%%%s%%"
                               OR district LIKE "%%%s%%"''' %(TABLE_NAME, name, name, name,)
        # print sql
        count = cursor.execute(sql)
        if count > 0:
            realWants = cursor.fetchone()
            print name
            print item['link']
            print realWants
            try:
                secretaryList, mayerList = MDPraseDetail.downUrlRetrieve(item['link'])
            except Exception, e:
                print 'error............'
                print e
                pass
            # print secretaryList
            # print mayerList
            for secretary in secretaryList:
                try:
                    # forTime = 'None'
                    # sufTime = 'None'
                    position = realWants['province']
                    if realWants['city'] !='None' and realWants['city'] != None:
                        position = realWants['city']
                    if realWants['district'] !='None' and realWants['district'] != None:
                        position = realWants['district']
                    try:
                        forTime = secretary['forTime']
                    except:
                        forTime = 'None'
                    try:
                        sufTime = secretary['sufTime']
                    except:
                        sufTime = 'None'
                    print secretary['name'][0], forTime, sufTime
                    insertSQL((secretary['name'][0], realWants['id'],
                               realWants['province'], realWants['city'],
                               realWants['district'], position + u'书记',
                               forTime, sufTime))

                except Exception, e:
                    print e
                    print 'no startTime'

            for mayer in mayerList:
                try:
                    # forTime = 'None'
                    # sufTime = 'None'
                    position = realWants['province']
                    if realWants['city'] !='None' and realWants['city'] != None:
                        position = realWants['city']
                    if realWants['district'] !='None' and realWants['district'] != None:
                        position = realWants['district']
                    try:
                        forTime = mayer['forTime']
                    except:
                        forTime = 'None'
                    try:
                        sufTime = mayer['sufTime']
                    except:
                        sufTime = 'None'
                    print mayer['name'][0], forTime, sufTime
                    insertSQL((mayer['name'][0], realWants['id'],
                               realWants['province'], realWants['city'],
                               realWants['district'], position + u'长',
                               forTime, sufTime))
                except Exception, e:
                    print e
                    print 'no startTime'


if __name__ == "__main__":
    getLinkAndArea()