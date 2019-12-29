# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from fake_useragent import UserAgent
from urllib import parse


class EmploySpider(scrapy.Spider):
    name = 'employ'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1566266592644&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1566266695175&postId={}&language=zh-cn'
    key = input("请输入要搜索的职位")
    position = parse.quote(key)
    headers = {'User-Agent': UserAgent().random}

    def start_requests(self):
        # 获取总页数
        num = self.get_total()
        for i in range(1, num + 1):
            result = self.one_url.format(self.position, i)
            yield scrapy.Request(url=result, callback=self.parse_one)

    def get_total(self):
        """获取keyword类别的总页数"""
        url = self.one_url.format(self.position, 1)
        html = requests.get(url=url, headers=self.headers).json()
        print(html)
        count = html['Data']['Count']
        if count % 10 == 0:
            total = count // 10
        else:
            total = count // 10 + 1
        return total

    def parse_one(self, response):
        html = json.loads(response.text)
        url_list = html['Data']['Posts']
        for i in url_list:
            key = i['PostId']
            result = self.two_url.format(key)
            yield scrapy.Request(url=result, callback=self.parse_two)

    def parse_two(self, response):
        # Data: {PostId: "1189442196059721728", RecruitPostId: 54715, RecruitPostName: "25923-云游戏高级技术运营工程师",…}
        # RecruitPostName: "25923-云游戏高级技术运营工程师"
        # LocationName: "深圳"
        # OuterPostTypeID: "40001003"
        # CategoryName: "技术"
        # Responsibility: "1.负责云游戏平台搭建，技术支持以及日常运维。↵2.以产品为核心，用户体验为导向，不断通过技术优化服务质量、成本，并提升云游戏服务的可运维性。↵3.积极拥抱新技术演进包括5G、边缘计算等等，并进行技术运营上的探索和挖掘，找到新技术和产品结合点，并推进落地。↵4.与项目组建立良好的合作沟通与信任关系，对业务存在的风险问题进行定期反馈和改善跟进，保障服务稳定运行；"
        # Requirement: "1. 计算机相关专业本科及以上学历；↵2. 对Linux、Windows系统原理较为了解，精通脚本语言（Python/Perl/Golang/Shell至少两种以上）； ↵3. 熟悉虚拟化技术如KVM/XEN/LXC等技术原理，有相应的运维及管理实践经验优先；↵4. 熟悉微服务框架、Docker、K8S架构，有实际应用经验者优先； ↵5. 熟悉开源存储分布式架构，有海量服务及高并发系统运维经验者优先；  ↵6. 要求学习能力强，具备优秀的逻辑思维能力，对解决挑战性问题充满热情，善于解决问题和分析问题，有主动服务意识。"
        # LastUpdateTime: "2019年12月26日"
        from ..items import EmployspiderItem
        # name = scrapy.Field()  # 名称
        # site = scrapy.Field()  # 地点
        # type = scrapy.Field()  # 类型
        # update_time = scrapy.Field()  # 发布日期
        # duty = scrapy.Field()  # 工作职责
        # claim = scrapy.Field()  # 工作要求
        item = EmployspiderItem()
        html = json.loads(response.text)
        item['name'] = html['Data']['RecruitPostName']
        item['site'] = html['Data']['LocationName']
        item['type'] = html['Data']['CategoryName']
        item['update_time'] = html['Data']['LastUpdateTime']
        item['duty'] = html['Data']['Responsibility']
        item['claim'] = html['Data']['Requirement']
        item['key'] = self.key
        item['stem_from'] = '腾讯招聘'
        yield item
