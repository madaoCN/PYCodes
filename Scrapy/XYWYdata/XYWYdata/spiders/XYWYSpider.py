#!/usr/bin/python
# -*- coding=utf8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from XYWYdata.items import XywydataItem
import sys, re, math, string

class XYWYSpider(Spider):
    name = "xywy"
    allowed_domains = ["z.xywy.com"]
    start_urls = [
        # 山东
# 'http://z.xywy.com/yiyuandiqu-shandong.htm'
#         # 山西
# 'http://z.xywy.com/yiyuandiqu-shanxisheng.htm',
# # 河北
# 'http://z.xywy.com/yiyuandiqu-hebei.htm',
# # 河南
# 'http://z.xywy.com/yiyuandiqu-henan.htm',
# # 天津
# 'http://z.xywy.com/yiyuandiqu-tianjin.htm',
# # 辽宁
# 'http://z.xywy.com/yiyuandiqu-liaoning.htm',
# # 黑龙江
# 'http://z.xywy.com/yiyuandiqu-heilongjiang.htm',
# # 吉林
# 'http://z.xywy.com/yiyuandiqu-jilin.htm',
# # 湖北
# 'http://z.xywy.com/yiyuandiqu-hubei.htm',
# # 湖南
# 'http://z.xywy.com/yiyuandiqu-hunan.htm',
# # 四川
# 'http://z.xywy.com/yiyuandiqu-sichuan.htm',
# # 重庆
# 'http://z.xywy.com/yiyuandiqu-chongqing.htm',
# # 陕西
# 'http://z.xywy.com/yiyuandiqu-shanxi.htm',
# # 甘肃
# 'http://z.xywy.com/yiyuandiqu-gansu.htm',
# # 云南
# 'http://z.xywy.com/yiyuandiqu-yunnan.htm',
# # 新疆
# 'http://z.xywy.com/yiyuandiqu-xinjiang.htm',
# 内蒙古
'http://z.xywy.com/yiyuandiqu-neimenggu.htm',
# # 海南
# 'http://z.xywy.com/yiyuandiqu-hainan.htm',
# # 贵州
# 'http://z.xywy.com/yiyuandiqu-guizhou.htm',
# # 青海
# 'http://z.xywy.com/yiyuandiqu-qinghai.htm',
# # 宁夏
# 'http://z.xywy.com/yiyuandiqu-ningxia.htm',
# # 西藏
'http://z.xywy.com/yiyuandiqu-xizang.htm',
]

    def parse(self, response):
        # 初始化选择器
        sel = Selector(response)
        # links = sel.xpath("//ul[@class='clearfix']/li/a/@href").extract()
        links = sel.xpath("//div[@class='pb10 pl30 bdr-dashed pt10 oh clearfix']")

        # print len(links)
        for link in links:
            area = link.xpath("div[@class='zh-impor-area f18 fYaHei']/text()").extract()
            nextLinks = link.xpath("div[2]/ul[@class='clearfix']//li/a/@href").extract()
            # print len(nextLinks)
            flag = 0
            for nextLink in nextLinks:
                item = XywydataItem()
                item['area'] = area[0]
                yield Request(str(nextLink), meta={'item':item},callback=self.parse_keshi)

        #获取二级页面的URL
    def parse_keshi(self, response):
        sel = Selector(response)
        links = sel.xpath("//span[@class='gray gray-a']/a/@href").extract()
        num = sel.xpath("//span[@class='gray gray-a']/a/text()").extract()
        item = XywydataItem()
        flag = 0
        # 传递参数
        item = response.meta['item']
        for link in links:
            print "++++++++++++++科室" + str(link)
            # item['link'] = str(link)
            num_ = num[flag]
            link_ = str(link)
            # item['nums'] = num_.encode("UTF-8", 'ignore')
            num_2 = (num_.encode("UTF-8", 'ignore')).strip('位')
            flag += 1
            print num_2
            for i in range(1, (int(num_2)+19)/20 + 1):
                if i == 1:
                    yield Request(link, meta={'item':item},callback=self.parse_doctor)
                else:
                    link_2 = link_ + "?page=%s" % i
                    yield Request(link_2, meta={'item':item},callback=self.parse_doctor)

            # yield item

    # 获取三级页面
    def parse_doctor(self, response):
        # 初始化选择器
        sel = Selector(response)
        links = sel.xpath("//div[@class='schedule-list clearfix pt15 pb20 pl10 pr10 bdr-botd graydeep']/div/a/@href").extract()
        # item = XywydataItem()
        item = response.meta['item']
        for link in links:
            print "++++++++++++++医生" + str(link)
            # item['link'] = link
            yield Request(str(link), meta={'item':item},callback=self.parse_final)


    # 解析最终环节!
    def parse_final(self, response):
        # 初始化选择器
        sel = Selector(response)
        item = response.meta['item']
        # 姓名
        name = sel.xpath("//div[@class='z-head-name']/strong/a/text()").extract()
        # # 地区
        # area = sel.xpath("").extract()
        docInfo = sel.xpath("//div[@class='doctor-page-infor-txt fl ml20 lh28']")
        # 医院
        hostpital = (docInfo[0]).xpath("div[1]/span[2]/a/text()").extract()
        # 科室
        office = (docInfo[0]).xpath("div[1]/span[3]/a/text()").extract()
        # # 职称
        proTitle = (docInfo[0]).xpath("div[2]/span[2]/text()").extract()

        tel = sel.xpath("//div[@class='doctor-contact-phone clearfix']")
        telNum = tel.xpath("div/p[2]/span[@style='color:#f0931a;font-weight:700']/text()").extract()
        # if len(telNum) != 0:
        #     print telNum
        # else:
        #     print "空"
        # # 预约加号人数
        appointment = sel.xpath("//div[@class='doctor-contact-appointment clearfix']")
        appointmentNum = appointment.xpath("div/p[2]/span[@style='color:#f0931a;font-weight:700']/text()").extract()
        # if len(appointmentNum) != 0:
        #     print appointmentNum
        # else:
        #     print "空"
        # # 图文咨询人数
        gra = sel.xpath("//div[@class='doctor-contact-tuw clearfix']")
        graNum = gra.xpath("div/p[2]/span[@style='color:#f0931a;font-weight:700']/text()").extract()
        # if len(graNum) != 0:
        #     print graNum
        # else:
        #     print "空"
        # # # 预约加号人数
        # appointment = sel.xpath("//di[@class='doctor-contact-appointment clearfix']")
        # appointmentNum = appointment.xpath("//span[@style='color:#f0931a;font-weight:700']/text()").extract()
        # print appointmentNum
        # # # 图文咨询人数
        # gra = sel.xpath("//div[@class='doctor-contact-tuw clearfix']")
        # graNum = gra.xpath("//span[@style='color:#f0931a;font-weight:700']/text()").extract()
        # 初始化数据模型
        # print graNum
        item['name'] = name[0]
        item['hospital'] = hostpital[0]
        item['office'] = office[0]
        if len(proTitle) != 0:
            item['proTitle'] = proTitle[0]
        else:
            item['proTitle'] = '-1'
        if len(telNum) != 0:
            item['telNum'] = telNum[0]
        else:
            item['telNum'] = '-1'
        if len(appointmentNum) != 0:
            item['appointmentNum'] = appointmentNum[0]
        else:
            item['appointmentNum'] = '-1'
        if len(graNum) != 0:
            item['graNum'] = graNum[0]
        else:
            item['graNum'] = '-1'
        yield item
