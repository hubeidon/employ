# -*- coding: utf-8 -*-
import time

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
        pass


    def parse(self, response):
        pass
