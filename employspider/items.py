# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmployspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 名称
    site = scrapy.Field()  # 地点
    type = scrapy.Field()  # 类型
    update_time = scrapy.Field()  # 发布日期
    duty = scrapy.Field()  # 工作职责
    claim = scrapy.Field()  # 工作要求
