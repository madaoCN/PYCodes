#!/usr/bin/python
# -*- coding:utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import request



class Spider(Spider):
    """爬取w3school标签"""
    #log.start("log",loglevel='INFO')
    name = "test"
    allowed_domains = ["z.xywy.com"]
    start_urls = [
        "http://z.xywy.com/zhuanjia-luhehospital-guke-zengjizhou.htm"
    ]

    def parse(self, response):
        sel = Selector(response)
        tel = sel.xpath("//div[@class='doctor-contact-phone clearfix']")
        telNum = tel.xpath("div/p[2]/span[@style='color:#f0931a;font-weight:700']/text()").extract()
        if len(telNum) != 0:
            print telNum
        else:
            print "空"
        # # 预约加号人数
        appointment = sel.xpath("//div[@class='doctor-contact-appointment clearfix']")
        appointmentNum = appointment.xpath("div/p[2]/span[@style='color:#f0931a;font-weight:700']/text()").extract()
        if len(appointmentNum) != 0:
            print appointmentNum
        else:
            print "空"
        # # 图文咨询人数
        gra = sel.xpath("//div[@class='doctor-contact-tuw clearfix']")
        graNum = gra.xpath("div/p[2]/span[@style='color:#f0931a;font-weight:700']/text()").extract()

        if len(graNum) != 0:
            print graNum
        else:
            print "空"
        # return items