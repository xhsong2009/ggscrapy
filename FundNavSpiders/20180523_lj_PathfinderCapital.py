# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-22

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request


class PathfinderCapitalSpider(GGFundNavSpider):
    name = 'FundNav_PathfinderCapital'
    sitename = '舍得之道资产'
    channel = '投顾净值'
    allowed_domains = ['www.msnfund.com']

    def start_requests(self):
        yield Request(url='http://www.msnfund.com/f/html/30/category-catid-30.html',
                      callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        fund_infos = response.xpath('//table[6]//tr//a')
        for fund_info in fund_infos:
            fund_url = fund_info.xpath(".//@href").extract_first()
            fund_name = fund_info.xpath(".//text()").extract_first()
            self.fps.append({
                'url': fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_fund(self, response):
        fund_name = response.meta['ext']['fund_name']
        fund_url = response.xpath("//a[contains(text(), '基金价格')]//@href").extract_first()
        self.ips.append({
            'url': fund_url,
            'ref': response.url,
            'ext': {'fund_name': fund_name}
        })

    def parse_item(self, response):
        rows = response.xpath('//table[@border="0"][@width="95%"]//td//p')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[5:]:
            fund_info = ''.join(row.xpath('.//span//text()').extract()).split()
            if len(fund_info) > 1:
                statistic_date = fund_info[0]
                nav = fund_info[1]
                added_nav = fund_info[2]
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

        rows = response.xpath('//table[@border="0"][@width="95%"]//td//div')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[5:]:
            fund_info = ''.join(row.xpath('.//span//text()').extract()).split()
            if len(fund_info) > 1:
                statistic_date = fund_info[0]
                nav = fund_info[1]
                added_nav = fund_info[2]
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

