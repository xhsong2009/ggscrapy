# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class PuYuanZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_PuYuanZiChanInvest'
    sitename = '璞远资产'
    channel = '投顾净值'
    allowed_domains = ['www.capnext.cn']

    fps = [{'url': 'http://www.capnext.cn/product'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[2]//tr//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.capnext.cn' + fund_url,
                'ref': response.url,
            })

    def parse_item(self, response):
        categories = re.findall('categories: \[(.*?)\]', response.text)[0]
        nav_info = re.findall('data:\[(.*?)\]', response.text)[0]
        statistic_dates = categories.split(',')
        navs = nav_info.split(',')
        fund_name = response.xpath("//h1[@class='articleh1']//text()").extract_first()
        for row in zip(statistic_dates, navs):
            statistic_date = row[0].replace("'", "")
            nav = row[1]
            added_nav = row[1]
            if statistic_date:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
