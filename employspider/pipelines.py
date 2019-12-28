# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class EmployspiderPipeline(object):
    # def open_spider(self,spider):
    #     self.db = pymysql.connect('localhost','root','990430','employ',charset='utf8')
    #     self.cur = self.db.cursor()
    #
    #
    # def process_item(self,item,spider):
    #     ins='insert into tencenttab values(%s,%s,%s,%s,%s,%s)'
    #     # name = scrapy.Field()  # 名称
    #     # site = scrapy.Field()  # 地点
    #     # type = scrapy.Field()  # 类型
    #     # update_time = scrapy.Field()  # 发布日期
    #     # duty = scrapy.Field()  # 工作职责
    #     # claim = scrapy.Field()  # 工作要求
    #     L = [
    #         item['name'],
    #         item['site'],
    #         item['type'],
    #         item['update_time'],
    #         item['duty'],
    #         item['claim']
    #     ]
    #     self.cur.execute(ins,L)
    #     self.db.commit()
    #     return item
    #
    # def close_spider(self,spider):
    #     self.cur.close()
    #     self.db.close()
    def process_item(self,item,spider):
        print(item)
        return item



