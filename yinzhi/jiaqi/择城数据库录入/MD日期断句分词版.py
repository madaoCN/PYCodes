# coding=utf8
import os
import codecs
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import jieba
import jieba.analyse
import jieba.posseg as pseg

resultDIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'jieba')

compiler1 = re.compile(u'(?<![(/p)(/wp)(/v)(/w)])\s(?P<year>(19\d{2}|20\d{2})[年])')
def breakSentencesByYear(sentence):
    '''
    按年份分词
    :param sentence:
    :return:
    '''
    # seg_list = jieba.cut(sentence.strip(), HMM=True)
    seg_list = []
    seg_set = pseg.cut(sentence.strip(), HMM=True)
    for word, flag in seg_set:
        # print('%s %s' % (word, flag))
        seg_list.append(word + '/' + flag)
    return ' '.join(seg_list)

def breakSentenceByTag(sentence):
    sentence = compiler1.sub('## \g<year>', sentence)
    seg_set = sentence.split("##")
    return seg_set

def breakWords(dire, fileName):
    '''
    分词脚本
    :param dire:
    :param fileName:
    :return:
    '''
    # currentDIR = os.path.dirname(filePath)
    filePath = os.path.join(dire, fileName)#sentences文件地址
    resultFile = codecs.open(os.path.join(resultDIR, fileName),'w+', 'utf8')#目标存储文件地址
    with codecs.open(filePath, encoding='utf8') as file:
        sentenceList= []
        for line in file.readlines():
            line = line.strip()
            # sentenceList.extend(breakSentencesByYear(line))
            sentenceList.extend(breakSentenceByTag(line))
        for sentence in sentenceList:
            sentence = sentence.strip()
            if len(sentence)  > 3:
                resultFile.write(sentence + '\n')

def main(dire, file):
    try:
        # contetnt = getFileContent(os.path.join(dire, file))
        breakWords(dire, file)
    except Exception, e:
        print '**********' + file + '**********'
        print e


if __name__ == "__main__":
    if not os.path.exists(resultDIR):
        os.makedirs(resultDIR)
    # jieba.enable_parallel(4)#并行分词
    # pool = Pool(5)
    # def funx(args, dire ,files):
    #     for file in files:
    #         if file.endswith('.txt'):
    #             # pool.apply_async(main, (dire, file))
    #             main(dire, file)
    # os.path.walk('/Users/liangxiansong/Desktop/test', funx, ())
    # pool.close()
    # pool.join()

    direPath = os.path.join('/Users/liangxiansong/Desktop/test')
    folderPath = os.path.join('/Users/liangxiansong/Desktop/target.txt')
    with codecs.open(folderPath, 'r', 'utf8') as file:
        for lines in file.readlines():
            lines = lines.strip()
            main(direPath, lines)
