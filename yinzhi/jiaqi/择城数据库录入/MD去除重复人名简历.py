#coding= utf8

import codecs
import os
import re


def doSomething(filePath, fliterPath, resultPath):
    dateSet = {}
    fliterFile = codecs.open(fliterPath, 'w+', 'utf8')
    resultFile = codecs.open(resultPath, 'w+', 'utf8')

    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            print line
            if line.endswith(".txt") and not line.endswith('er.txt'):
                hmName = line.split("/")[-1].split('_')[1]
                # print re.search(u'代.*?长', hmName)
                if not re.search(u'[\(\（].*?代.*?[\)\）]', hmName) and not re.search(u'.*?代.*?长', hmName):
                    dirPath = os.path.dirname(filePath)
                    size = os.path.getsize(os.path.join(dirPath, line.lstrip('./')))
                    hmName = hmName.split(u'（')[0].split(u'(')[0]
                    if size > 0 and not dateSet.has_key(hmName + '_' + str(size)):
                        dateSet[hmName + '_' + str(size)] = line
                    else:
                        fliterFile.write(line + '\n')
                else:
                    fliterFile.write(line + '\n')

    for key in dateSet.keys():
        print key
        resultFile.write(dateSet.get(key) + '\n')

def deleteFile(fiterPath):
    dirPath = os.path.dirname(fiterPath)
    with codecs.open(fiterPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            if line.endswith(".txt"):
                line = os.path.join(dirPath, line.lstrip('./'))
                print line
                os.remove(line)



if __name__ == "__main__":
    # filePath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'folder.txt')
    fliterPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'fliter.txt')
    # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'result.txt')
    # doSomething(filePath, fliterPath, resultPath)
    deleteFile(fliterPath)