# coding=

import csv, codecs
with codecs.open("test.csv", "w+", 'gbk') as file:
    writer = csv.writer(file)
    writer.writerow(('num','like'))
    writer.writerow(["哈哈哈", "什么鬼"])