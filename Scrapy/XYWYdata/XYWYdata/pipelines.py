# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re, json, codecs,csv
import sys

class XywydataPipeline(object):
    def __init__(self):
        self.file = codecs.open("内蒙古.txt", "a", encoding="utf-8")
    def process_item(self, item, spider):
        write = csv.writer(self.file)

        reload(sys)
        sys.setdefaultencoding('utf8')

        area =  (item["area"]).encode('utf-8')
        name = (item['name'])
        hospital = item['hospital']
        office = item['office']
        proTitle = item['proTitle']
        telNum = item['telNum']
        appointmentNum = item['appointmentNum']
        graNum = item['graNum']
        print "===================" + area
        print "===================" + name
        print "===================" + hospital
        write.writerow((name, area, hospital, office, proTitle, telNum, appointmentNum, graNum))
        return item