#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool
from SentenceModel import SententceModel
from MDError import MDError
import uuid
import MySQLdb as mdb
import pymongo

IDX = 0

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'toor',
    'db': 'zeCheng',
    'charset': 'utf8'
}
conn = mdb.connect(**config)
#获取游标
cursor = conn.cursor()

# import sys
# reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
# sys.setdefaultencoding('utf-8')
OUT_FILE_DIR = os.path.join(os.path.expanduser("~"), 'Desktop', 'out-v2')
FILE = codecs.open(os.path.join(os.path.expanduser("~"), 'Desktop', 'result.txt'), 'a', 'utf8')

def reverseFile(filePath):
    '''
    遍历文件
    :param filePath: 文件路径
    :return: 句子列表
    '''
    sentenceList = []
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            sentenceList.append(line)

    return sentenceList

def getFileContent(filePath):
    '''
    遍历文件
    :param filePath: 文件路径
    :return: 句子列表
    '''
    with codecs.open(filePath, 'r', 'utf8') as file:
        return file.read()

    return None

def findYear(strline):
    '''
    判断是否带有年份
    :param strline:
    :return:
    '''
    # print len(re.findall(u'(\d{2})(?=年)', strline)) == 0
    # print re.findall(u'(\d{2})(?=年)', strline)
    return False if len(re.findall(u'(\d{2})(?=年)', strline)) == 0 else True

def judgeYear(str):
    '''
    判断是否含1940以前年的信息
    :param str:
    :return:
    '''
    # print re.findall(u'(19[0-3]\d|40)(?=年)', str)
    # print len(re.findall(u'(19[0-3]\d|40)(?=年)', str))
    return False if len(re.findall(u'(19[0-3]\d|40)(?=年)', str)) == 0 else True

def praseTagSet(strline):
    '''
    抓取分词标签
    :param strline:
    :return:
    '''
    result = re.findall('(/.+?\\b)', strline)
    str = '_'.join(result)
    str = str.replace('/', '')
    return str

def removeTag(strline):
    '''
    去除标签
    :param strline:
    :return:
    '''
    result = re.sub('(/.+?\\b)', "_", strline).replace(' ', '')
    # str = '_'.join(result)
    # str = str.replace('/', '')
    return result

def mapSenteceToModels(hmName ,hmId ,fileName, origSts, tagSets):
    '''
    映射模型
    '''
    modelList = []
    for index in range(len(origSts)):#遍历原句列表
        stModel = SententceModel()
        stModel.stId = str(hmId).zfill(4) + '_' + str(index).zfill(4)
        stModel.hmName = hmName
        stModel.fileName = fileName
        stModel.hmId = str(hmId).zfill(4)
        stModel.origSt = origSts[index].encode('utf8')
        stModel.clearSt = removeTag(tagSets[index]).encode('utf8')
        stModel.splitSt = tagSets[index].encode('utf8')
        stModel.tagSet = praseTagSet(tagSets[index]).encode('utf8')
        stModel.hasYear = u'True' if findYear(origSts[index]) else u'False'
        modelList.append(stModel)
    return modelList

def loadToDB(stModel):
    '''
    录入数据库
    :param stModel:
    :return:
    '''
    sql = 'INSERT INTO t_CaeerInfo (stId, hmName, ' \
                                    'hmId, fileName, ' \
                                    'origSt, splitTagSt, ' \
                                    'tagSet, splitOrigSt,' \
                                    'hasYear) ' \
          'values("%s","%s","%s","%s","%s","%s","%s","%s", "%s")' \
          % (mdb.escape_string(stModel.stId), mdb.escape_string(stModel.hmName),
             mdb.escape_string(stModel.hmId), mdb.escape_string(stModel.fileName),
             mdb.escape_string(stModel.origSt), mdb.escape_string(stModel.splitSt),
             mdb.escape_string(stModel.tagSet), mdb.escape_string(stModel.clearSt),
             mdb.escape_string(stModel.hasYear))
    # print sql
    cursor.execute(sql)
    conn.commit()

def main(dire, file):
    # print dire, file
    global IDX
    IDX = IDX + 1
    # hmId = uuid.uuid1()
    try:
        fileName = file
        hmName = None
        oriList = []
        splitList = []
        modelList = []
        splitPath = os.path.join(OUT_FILE_DIR, fileName)
        orginPath = os.path.join(dire, file)
        hmName = re.search('_(?P<name>.+?)_', fileName).group("name")
        if os.path.exists(splitPath) and os.path.exists(orginPath):

            if judgeYear(getFileContent(orginPath)):
                print '包含1940年前的信息 跳过'
                print '**********' + file + '**********'
                return
                #----------------------原句
            oriList = reverseFile(orginPath)
        #----------------------分词后句
            splitList = reverseFile(splitPath)
            if len(oriList) != len(splitList):
                raise MDError("原始句子数目和粉刺后句子数目不一致")

        else:
            raise MDError("文件不存在")

        modelList = mapSenteceToModels(hmName, IDX, file, oriList, splitList)

        for item in modelList:
            # pass
            # print item.hasYear
            # print item.origSt
            loadToDB(item)
            # FILE.write(item.hmName.decode('utf8'))
            # FILE.write(item.hmName.decode('utf8') + '##'
            #            + str(item.hmId) + '##'
            #            +item.stId.decode('utf8') + '##'
            #            +item.origSt.decode('utf8') + '##'
            #            + item.clearSt + '##'
            #            +item.splitSt.decode('utf8') + '##'
            #            +item.tagSet + '##'
            #            +item.fileName.decode('utf8') + '\n')
    except MDError, e:
        print e
        print '**********' + file + '**********'
    except Exception, e:
        print e
        print '**********' + file + '**********'



if __name__ == "__main__":
    # pool = Pool(5)
    # def funx(args, dire ,files):
    #     for file in files:
    #         if file.endswith('.txt'):
    #             pool.apply_async(main, (dire, file))
    #
    # os.path.walk('/Users/liangxiansong/Desktop/sentences/', funx, ())
    # pool.close()
    # pool.join()

    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.txt'):
                main(dire, file)

    os.path.walk('/Users/liangxiansong/Desktop/sentences/', funx, ())


