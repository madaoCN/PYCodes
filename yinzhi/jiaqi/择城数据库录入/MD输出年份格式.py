#coding= utf8

import codecs
import os
import re

def replaceItem(content):
    print re.findall('.{1}[\d{1,4}]{1,4}.{1}', content)
    return re.findall('.{1}[\d{1,4}]{1,4}.{1}', content)

def doSomething(resultPath, dirPath):
    targetPath = os.path.join(dirPath, )
    with codecs.open(resultPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            if line.endswith(".txt") and not line.endswith("t.txt") and not line.endswith("r.txt"):
                print os.path.join(dirPath, line.lstrip('./'))
                with codecs.open(os.path.join(dirPath, line.lstrip('./')), 'r', 'utf8') as resultFile:
                    content = resultFile.read()
                    list = replaceItem(content)
                    with codecs.open(os.path.join(dirPath, 'target.txt'), 'a', 'utf8') as modifyFile:
                        for item in list:
                            modifyFile.write(item)
                            modifyFile.write('\n')
if __name__ == "__main__":

    resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences', 'result.txt')
    dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences')

    # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'result.txt')
    # dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test')

    doSomething(resultPath, dirPath)