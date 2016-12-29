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
from MDSort import MDSort
from MDStack import Stack


TOTAL_NUM = 166310
cpYear = re.compile('(?<![a-zA-Z])year')
cpNt = re.compile('(?<![a-zA-Z])nt(?=[_])')
cpPosition = re.compile('(?<![a-zA-Z])nposition(?=[_])')

def main():
    FILE = codecs.open("/Users/liangxiansong/Desktop/target.txt", "a", "utf8")
    mdMap = {}
    contentPath = os.path.join(os.path.expanduser("~"), "Desktop", 'result_out.txt')
    with codecs.open(contentPath, 'r', 'utf8') as file:
        for line in file.readlines():
            key = line.split("##")[1]
            mdMap[key] = line
        print len(mdMap)

    idPath = os.path.join(os.path.expanduser("~"), "Desktop", 'ids.txt')
    with codecs.open(idPath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip()
            FILE.write(mdMap.pop(line))



if __name__ == "__main__":
    main()