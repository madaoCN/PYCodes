# coding=utf8
# !/usr/bin/env python
import MySQLdb as mdb
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from threading import Timer
import time
import codecs
import os
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 创建一个logger
logger = logging.getLogger('MDSpider')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('spyLIXIN.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

config = {
    'host': '202.120.24.211',
    'port': 3306,
    'user': 'root',
    'passwd': 'YinZhi518',
    'db': 'focusns_prod',
    'charset': 'utf8'
}

SQLAssignmentID2FindTeacherName = '''SELECT name FROM tb_teacher WHERE id in
(SELECT fk_teacher_id FROM tb_course where id=%s)'''
SQLId2NameANDNAME = '''SELECT name,student_no from tb_student WHERE id in
(SELECT fk_student_id FROM tb_testpaper where id=%s)'''

TEACHERSET = set()
STUDENTSET = set()


def writeLog(content):
    currentDir = os.getcwd()
    with codecs.open(os.path.join(currentDir, 'log.txt'), 'a') as file:
        file.write(content)
        file.write('\n')
    file.close


def ConfigInitialData(tearcher, student):
    tearchSet = set()
    studentSet = set()
    conn = mdb.connect(**config)
    cursor = conn.cursor()
    # fliterList = [69, 70, 71, 72, 73, 74, 75, 76]
    fliterList = []

    if tearcher != None:
        cursor.execute('SELECT id,fk_course_id,name from tb_assignment')
        for item in cursor.fetchall():  # 教师出题
            if item[1] in fliterList:
                continue
            tearchSet.add(str(item[0]) + '#' + str(item[1]) + '#' + item[2])

    if student != None:
        cursor.execute('SELECT id,fk_assignment_id, curr_count, total_score from tb_testpaper')
        for item in cursor.fetchall():  # 学生答题
            studentSet.add(str(item[0]) + '#' + str(item[1]) + '#' + str(item[2]) + '#' + str(item[-1]))
    conn.close()

    return tearchSet, studentSet


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
        logger.info('发送邮件成功!!!')
    finally:
        smtp.close;


def FindTeacherDeliverWork():
    '''
    邵军是否出题
    :return:
    '''

    try:
        teacherSet, temp2 = ConfigInitialData(1, None)
        global TEACHERSET
        result = teacherSet - TEACHERSET

        nameList = []
        workNameList = []
        print len(result), len(teacherSet), len(TEACHERSET)
        if len(result):
            logger.info('有新作业发布啦')
            TEACHERSET = teacherSet
            conn = mdb.connect(**config)
            cursor = conn.cursor()
            for item in result:
                workNameList.append(item.split('#')[2])
                courseId = item.split('#')[1]
                cursor.execute(SQLAssignmentID2FindTeacherName % courseId)
                for item in cursor.fetchall():
                    nameList.append(item[0])
            conn.close()

            qStr = ''
            for idx in range(len(nameList)):
                print nameList[idx], workNameList[idx]
                qStr = qStr + u'\n' + nameList[idx] + u'发布了题目: %s' % workNameList[idx]

            logger.info(qStr)
            SendEmail("229377879@qq.com", u'教师发布了新题目!!!', qStr);
        else:
            logger.info('暂时没有新作业')


    except Exception, e:
        print 'error'
        logger.info(str(e))
        # writeLog(str(e))


def FindStudentWork():
    '''
    监测学生做题
    :return:
    '''
    try:
        temp1, studentSet = ConfigInitialData(None, 1)
        global STUDENTSET
        result = studentSet - STUDENTSET
        nameList = []
        curr_count = []
        studentNo = []
        total_score = []
        print len(result), len(studentSet), len(STUDENTSET)
        if len(result):
            logger.info('有学生做作业啦')
            STUDENTSET = studentSet
            conn = mdb.connect(**config)
            cursor = conn.cursor()
            for item in result:
                curr_count.append(item.split('#')[2])
                total_score.append(item.split('#')[-1])
                courseId = item.split('#')[0]
                cursor.execute(SQLId2NameANDNAME % courseId)
                for item in cursor.fetchall():
                    nameList.append(item[0])
                    studentNo.append(item[1])
            conn.close()

            qStr = ''
            for idx in range(len(studentNo)):
                print nameList[idx], studentNo[idx], curr_count[idx], total_score[idx]
                qStr = qStr + u'学生:%s 学号:%s 做题次数:%s 做题分数:%s' % (nameList[idx], studentNo[idx],
                                                                curr_count[idx], total_score[idx])
            logger.info(qStr)
            SendEmail("229377879@qq.com", u'学生做题啦!!!', qStr);
        else:
            logger.info('暂时没有学生做作业')
    except Exception, e:
        print 'error'
        logger.info(str(e))


def main():
    global TEACHERSET, STUDENTSET
    TEACHERSET, STUDENTSET = ConfigInitialData(1, 1)
    # FindTeacherDeliverWork()
    # FindStudentWork()
    # t = Timer(5, main)
    # t.start()
    while True:
        # logger.info(time.strftime('%Y-%m-%d %X', time.localtime(time.time())))
        FindTeacherDeliverWork()
        FindStudentWork()
        time.sleep(60 * 10)


if __name__ == "__main__":
    main()





