# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
import csv

class W3SchoolPipeline(object):

    def __init__(self):
        self.file = codecs.open("w3school_data_utf8.csv", "w+", encoding="utf-8")
    def process_item(self, item, spider):
        write = csv.writer(self.file)
        it = dict[item]
        a = item['title']
        b = item['link']
        c = item['desc']
        print type(item)
        write.writerow((a, b, c))

    # def __init__(self):
    #     self.file = codecs.open('w3school_data_utf8.csv', 'wb', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     line = json.dumps(dict(item)) + '\n'
    #     # print line
    #     self.file.write(line.decode("unicode_escape"))
    #     return item