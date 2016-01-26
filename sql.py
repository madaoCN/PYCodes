# coding=utf-8
#导入pymysql的包
import pymysql
try:
#获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
    conn=pymysql.connect(host='localhost',user='root',passwd='123456',port=3306,charset='utf8')
    cur=conn.cursor()                              #获取一个游标对象
    # cur.execute("CREATE DATABASE test15")          #执行对应的SQL语句
    cur.execute("USE test15")
    # cur.execute("CREATE TABLE users (id INT, name VARCHAR(18))")
    cur.execute("INSERT INTO users VALUES(1, 'blog')")

 
    cur.execute("SELECT * FROM users")
    data=cur.fetchall()

    for row in data:
        print '%s\t%s' %row



    cur.close()                                    #关闭游标
    conn.commit()                                  #向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    conn.close()                                   #关闭到数据库的连接，释放数据库资源
except  Exception :
    print("发生异常")