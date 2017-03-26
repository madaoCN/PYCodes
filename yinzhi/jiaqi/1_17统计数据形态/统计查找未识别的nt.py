#coding=utf8
import codecs
import os
import re
import ConfigParser
from collections import deque

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

RESUTL_LIST = []
find_NP_complier = re.compile(u'/nposition\\b')
find_NS_complier = re.compile(u'/ns\\b')
find_NT_complier = re.compile(u'/nt\\b')
find_Blank_complier = re.compile(u'\/')


def find_something(sentence, sentenceID):
    ''''''
    stack = []
    splitSentence = sentence.split(' ')
    #过滤机构nt
    splitSentence = filter(lambda item:not find_NT_complier.search(item), splitSentence)
    for item in splitSentence:
        if find_NS_complier.search(item):#是ns
            if len(stack) and find_NP_complier.search(stack[0]):#stack第一个元素是NP
                stack.append(item)
                stack.insert(0, sentenceID)
                RESUTL_LIST.append(stack[:])
                del stack[:]
                stack.append(item)
            elif len(stack) and find_NS_complier.search(stack[0]):#stack第一个元素也是NS
                del stack[:]
                stack.append(item)
            else:
                stack.append(item)
        elif find_NP_complier.search(item): #是np
            if len(stack) and find_NS_complier.search(stack[0]):##stack第一个元素是NS
                stack.append(item)
                stack.insert(0, sentenceID)
                RESUTL_LIST.append(stack[:])
                del stack[:]
                stack.append(item)
            elif len(stack) and find_NP_complier.search(stack[0]):#stack第一个元素也是NP
                del stack[:]
                stack.append(item)
            else:
                stack.append(item)
        else:#普通字符
            if len(stack) and (find_NS_complier.search(stack[0]) or find_NP_complier.search(stack[0])):
                stack.append(item)

if __name__ == "__main__":
    inputPath = cf.get('find_unRecognize', 'input_path')
    outPath = cf.get('find_unRecognize', 'out_path')
    # with codecs.open(inputPath, 'r', 'utf8') as file:
    #     for line in file.xreadlines():
    #         splitList = line.split('##')
    #         sentence = splitList[6]
    #         sentenceID = splitList[3]
    #         find_something(sentence, sentenceID)
    # # print len(RESUTL_LIST)
    # with codecs.open(outPath, 'a', ) as file:
    #     map(lambda lines: file.write('  '.join(lines) + '\n'), RESUTL_LIST)

    with codecs.open(outPath, 'r', 'utf8') as file:
        with codecs.open('data/test.txt', 'w') as outFile:
            for line in file.xreadlines():
                if len(find_Blank_complier.findall(line)) > 2:
                    outFile.write(line)


