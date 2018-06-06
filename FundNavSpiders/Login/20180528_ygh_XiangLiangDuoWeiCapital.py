# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-28


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest


class XiangLiangDuoWeiCapitalSpider(GGFundNavSpider):
    name = 'FundNav_XiangLiangDuoWeiCapital'
    sitename = '北京向量多维资本'
    channel = '投顾净值'
    allowed_domains = ['www.xiangliangfund.com']

    username = '薛熙茂'
    password = '123456'

    fps = [{
        'url': 'http://www.xiangliangfund.com/?a=cp&id=1'
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.xiangliangfund.com/?a=dodl',
                          formdata={
                              'name': self.username,
                              'pwd': self.password
                          })

    def parse_fund(self, response):
        funds = response.xpath('//ul[@class = "menu"]//li//@href').extract()
        for f_url in funds:
            self.ips.append({
                'url': 'http://www.xiangliangfund.com' + f_url,
                'ref': response.url
            })

    def parse_item(self, response):
        f_list = response.xpath('//div[@class = "xian xian1"]/table[2]//tr')
        for i in f_list[1:]:
            t = i.xpath('td//text()').extract()
            fund_name = t[0]
            statistic_date = t[1]
            nav = t[2]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            yield item
