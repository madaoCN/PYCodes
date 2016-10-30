#coding=utf8

import MySQLdb as mdb
import pymongo
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from threading import  Timer
import time
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'Lxs123456',
    'db': 'test',
    'charset': 'utf8'
}

conn = mdb.connect(**config)
#获取游标
cursor = conn.cursor()

cursor.execute('SELECT count(*) from config WHERE id')
WORKCOUNT = cursor.fetchall()[0][0]

def SendEmail(toAdd, subject, text):
    # yvqkowkowrmmbcee
    strFrom = '591710552@qq.com';
    strTo = toAdd;
    msg = MIMEText(text, 'plain', 'utf8')
    # msg['Content-Type'] = 'Text/HTML';
    msg['Subject'] = Header(subject, 'utf8');
    msg['To'] = strTo;
    msg['From'] = strFrom;

    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465);
    smtp.login(strFrom, 'yvqkowkowrmmbcee');
    try:
        smtp.sendmail(strFrom, strTo, msg.as_string());
        print '发送邮件成功!!!'
    finally:
        smtp.close;

def FindEmail():
    print  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

    try:
        conn_2 = mdb.connect(**config)
        # 获取游标
        cursor_2 = conn_2.cursor()
        cursor_2.execute('SELECT count(*) from config WHERE id')
        count =  cursor_2.fetchall()[0][0]
        global WORKCOUNT
        print 'foremat:', WORKCOUNT, 'last:',count
        # if WORKCOUNT < count:
        #     print '发布了新作业'
        #     WORKCOUNT = count
        #     #查询记录
        #     cursor.execute('SELECT * from tb_assignment WHERE fk_course_id=73')
        #     for item in cursor.fetchall():
        #         workName = item[1]
        #         courseID = item[8]
        #         print workName, courseID
        #         SendEmail("1349963838@qq.com", "邵军操作", "邵军发布了题目:<<%s>>" % workName.encode('utf8'));
        #
        # else:
        #     print "没有变动"

                # SendEmail("1349963838@qq.com", "邵军操作", "邵军发布题目啦啦啦啦啦啦啦啦");
        cursor_2.close()
    except Exception, e:
        print 'error'
        print e

def main():
    # FindEmail()
    # t = Timer(1, main)
    # t.start()

    while True:
        FindEmail()
        time.sleep(4)


if __name__ == "__main__":
    main()






