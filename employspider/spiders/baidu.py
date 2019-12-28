# -*- coding: utf-8 -*-
import json
import time
from ..items import EmployspiderItem
import requests
import scrapy
from urllib import parse

from fake_useragent import UserAgent


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    # start_urls = ['http://www.baidu.com/']
    one_url = 'https://talent.baidu.com/baidu/web/httpservice/getPostList?postType=&workPlace={}&recruitType=2&keyWord={}&pageSize=10&curPage={}&_={}'
    key = parse.quote(input('请输入职位:'))
    headers = {'User-Agent': UserAgent().random}

    def start_requests(self):
        for i in ['0/4/7/9', '0/4/10/11', '0/4/204/207',
                  '0/4/248/249', '0/4/396/397', '0/4/396/399'
            , '0/4/396/432', '0/4/450/452', '0/4/43/52113720', '0/4/598/196769865', '0/4/90100/196769930']:
            count = self.get_num(i)
            for w in range(1,count+1):
                url = self.one_url.format(i,self.key,w,int(time.time()))
                yield scrapy.Request(url=url,callback=self.parse_one)

    def get_num(self, workPlace):
        # 北京:0/4/7/9
        # 上海:0/4/10/11
        # 杭州市:0/4/204/207
        # 福州市:0/4/248/249
        # 广州市:0/4/396/397
        # 深圳市:0/4/396/399
        # 东莞:0/4/396/432
        # 海口:0/4/450/452
        # 阳泉:0/4/43/52113720
        # 其他:0/4/598/196769865
        # 海外:0/4/90100/196769930
        i = parse.quote(workPlace)
        url = self.one_url.format(i, self.key, 1, int(time.time()))
        html = requests.get(url=url, headers=self.headers).json()
        count = html['rowCount']
        print(1111,i,count)
        if count % 10 == 0:
            total = count // 10
        else:
            total = count // 10 + 1
        return total

    def parse_one(self, response):
        html = json.loads(response.text)
        # postId: 144509
        # name: "语音技术部_语音服务开发工程师"
        # publishDate: "2019-12-23"
        # postType: "社招-T技术-标准"
        # workPlace: "北京市"
        # workYears: "不限"
        # recruitNum: 1
        # workType: "全职"
        # serviceCondition: "-熟悉c++/python/shell等编程语言
        # < br > -熟悉高并发线上集群服务的搭建和优化
        # < br > -了解常见的机器学习和自然语言处理算法
        # < br > -良好的团队合作和沟通能力，快速准确的理解能力，极强的自我驱动力，有一定的抗
        # 压能力，有责任心，对解决问题充满热情
        # "
        # workContent: "-负责语音识别产品中，前沿创新产品方向的架构搭建、开发、迭代等工作
        # < br > -根据产品需求及技术趋势，不断优化语音交互架构并保证服务稳定性
        # < br > -基于线上大规模数据，挖掘相关特征，提升语音交互体验
        # orgName: "百度"
        # replace(old, new[, max])
        item = EmployspiderItem()
        print(html['postList'][1]['workContent'].replace('<br>',''))
        for i in html['postList']:
            item['name'] = i['name']
            item['site'] = i['workPlace']
            item['type'] = i['postType']
            item['update_time'] = i['publishDate']
            item['duty'] = i['workContent'].replace('<br>','')
            item['claim'] = i['serviceCondition'].replace('<br>','')
            yield item

    def parse(self, response):
        pass
