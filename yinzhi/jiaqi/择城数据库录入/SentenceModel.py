#coding=utf8

class SententceModel:

    def __init__(self, hmName, hmId,stId, origSt, clearSt,splitSt, tagSet, fileName, hasYear):
        '''
        数据模型
        :param hmName: 人名
        :param stId: 句子ID
        :param origSt: 原句
        :param splitSt: 分词后
        :param tagSet: 标记集
        '''
        self.hmName = hmName
        self.hmId = hmId
        self.stId = stId
        self.origSt = origSt
        self.clearSt = clearSt
        self.splitSt = splitSt
        self.tagSet = tagSet
        self.fileName = fileName
        self.hasYear = hasYear



    def __init__(self):
        self.hmName = 'N/A'
        self.hmId = 'N/A'
        self.stId = 'N/A'
        self.origSt = 'N/A'
        self.clearSt = 'N/A'
        self.splitSt = 'N/A'
        self.tagSet = 'N/A'
        self.fileName = 'N/A'
        self.hasYear = 'False'
        self.sortedTag = 'N/A'


    def __repr__(self):
        return "hmName: " + self.hmName \
               + " hmID:" + self.hmId \
               + " stId:"   + self.stId \
               + " origSt:" + self.origSt \
               + " clearSt:" + self.clearSt \
               + " splitSt:" + self.splitSt \
               + " tagSet:" + self.tagSet \
               + " fileName:" + self.fileName\
               + " hasYear:" + self.hasYear \
               + " sortedTag:" + self.sortedTag


if __name__ == "__main__":

    import re
    print re.split(u'。|;|；', u'adsfasdf.sdfsdf。sadfsadf;fsdafsa；sadfsa')
