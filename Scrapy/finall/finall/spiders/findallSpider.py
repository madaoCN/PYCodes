# coding=utf8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
from  scrapy.selector import  Selector
from scrapy.item import Item
from scrapy.http import Request
from finall.items import FinallItem

class findallSpider(CrawlSpider):
    name = "links"
    allowed_domains = ["z.xywy.com"]
    start_urls = [
        # 从北京的页面开始爬
        "http://z.xywy.com/yiyuandiqu-beijing.htm"
    ]
    rules = [Rule(SgmlLinkExtractor(allow= (r"http://z\.xywy\.com/.+?\.htm")), callback="parse_item",follow=True)]

    def parse_item(self, response):
        sel = Selector(response)

        item = FinallItem()
        item["title"] = sel.xpath("/html/head/title").extract()

        return item
