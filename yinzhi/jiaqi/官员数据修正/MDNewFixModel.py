#coding=utf8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
class NewFixModel:

    def __init__(self):
        self.id = 'n/a' #id
        self.hmName = 'n/a' #人名
        self.hmId = 'n/a' #人ID
        self.sentenceId = 'n/a' #句子ID
        self.fileName = 'n/a' #文件名
        self.originSentence = 'n/a'  #原始句子
        self.splitedSentence = 'n/a' #分词后句子
        self.splitedTagSet = 'n/a' #分词后的tag集合 以'_' 联结
        self.splitedTextSet = 'n/a' #分词后的文本集合 以'_' 联结
        self.hasYear = 'False' #是否含有年份
        self.sortedTag = 'n/a' #tag排序
        self.yearNum = 'n/a' #年份数目
        self.ntNum = 'n/a' #nt 标签数目
        self.nPostionNum = 'n/a' #npostion 标签数目

    def __repr__(self):
        return '##'.join([self.id, self.hmName,
                          self.hmId, self.sentenceId,
                          self.fileName, self.originSentence,
                          self.splitedSentence, self.splitedTagSet,
                          self.splitedTextSet, self.hasYear,
                          self.sortedTag, self.yearNum,
                          self.ntNum, self.nPostionNum])

    def values(self):
        return '##'.join([self.id, self.hmName,
                          self.hmId, self.sentenceId,
                          self.fileName, self.originSentence,
                          self.splitedSentence])
