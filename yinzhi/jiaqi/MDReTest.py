#coding=utf8
import re
import jieba
from MDStack import Stack
import jieba.analyse

if __name__ == "__main__":
    string = u"1993.07—1997.07市长（其间：1994.09—1997.01 中共中央党校经济管理专业在职研究生学习 1996.09—1997.07 中共中央党校中青年干部培训班学习）"
    # string = u"1969年12月参加工作，南京工学院（现东南大学）本科毕业，中央党校研究生学历，高级经济师。"
    # seg_list = jieba.cut(string.strip())
    # print("Default Mode: " + "//".join(seg_list))  # 精确模式

    #处理 \d{2}年 的情况
    for item in re.findall(u'\d{2}年', string):
        string = string.replace(item, item[:-1] + u'#')
    seg_list = jieba.cut(string.strip().replace(u'—', u'#'))
    # print("Default Mode: " + "//".join(seg_list))  # 精确模式
    # 断句
    # divList = [li for li in seg_list]
    flag = 0
    mdStack = Stack()
    tempData = []
    tempStr = ''
    for li in seg_list:
        if li == ' ' and li == u'':
            pass
        if li != '#':
            mdStack.push(li)
        elif li == '#' and flag == 0:
            flag += 1
        elif li == "#" and flag > 0:
            temp = mdStack.pop()  # 抛出#号前一个
            while not mdStack.empty():
                tempData.append(mdStack.pop())
            tempData.reverse()
            tempStr = '#'.join(tempData)
            print tempStr
            print '=========='
            tempData = []
            mdStack.push(temp)

    tempData = []
    while not mdStack.empty():
        tempData.append(mdStack.pop())
    tempData.reverse()
    tempStr = '#'.join(tempData)
    print tempStr


    # seg_list = jieba.cut(string.strip().replace(u'—', u'#').replace(u'年', u'#'))
    # # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    # # 断句
    # # divList = [li for li in seg_list]
    # flag = 0
    # mdStack = Stack()
    # tempData = []
    # for li in seg_list:
    #     if li == ' ' and li == u'':
    #         pass
    #     if li != '#':
    #         mdStack.push(li)
    #     elif li == '#' and flag == 0:
    #         flag += 1
    #     elif li == "#" and flag > 0:
    #         temp = mdStack.pop()  # 抛出#号前一个
    #         while not mdStack.empty():
    #             tempData.append(mdStack.pop())
    #         tempData.reverse()
    #         print tempData
    #         tempData = []
    #         mdStack.push(temp)
    #
    # tempData = []
    # while not mdStack.empty():
    #     tempData.append(mdStack.pop())
    # tempData.reverse()
    # print tempData