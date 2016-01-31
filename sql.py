# coding=

import csv, codecs
with codecs.open("123.csv", "w+", 'gbk') as file:
    writer = csv.writer(file)
    writer.writerow(('num','like'))
    writer.writerow([1, 2])