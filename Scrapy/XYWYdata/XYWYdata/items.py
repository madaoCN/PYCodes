# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class XywydataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    area = Field()
    hospital = Field()
    office = Field()
    proTitle = Field()
    telNum =Field()
    appointmentNum = Field()
    graNum = Field()

