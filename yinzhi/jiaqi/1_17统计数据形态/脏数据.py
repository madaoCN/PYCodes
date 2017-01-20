#coding=utf8
import codecs
import os
import re
import chardet
from multiprocessing import Pool


if __name__ == "__main__":
    inputFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', '67482.txt')
    # divisionFilePath = os.path.join(os.path.expanduser('~'), 'Desktop', '1_17', 'division.txt')
    # Divisions.extend(loadFile(divisionFilePath))#读取区划
    # SpliteStr = "(" + '|'.join(Divisions) + ")"
    splitedSTList = []
    with codecs.open(inputFilePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            list = line.split("##")
            # splitedSTList.append(list[8])
            target = list[5]
            # print re.search('(省省|市市|区区|县县|州州)(委|长)', target)
            # if re.search(u'(省省|市市|区区|县县|州州)(委|长)', target):
            # if re.search(u'[\u4e00-\u9fa5]+?(省省|市市|区区|县县|州州)(委|长)', target):
            if re.search(u'，(省省|市市|区区|县县|州州)(委|长)', target):
                print target
                splitedSTList.append(target)
    print len(splitedSTList)