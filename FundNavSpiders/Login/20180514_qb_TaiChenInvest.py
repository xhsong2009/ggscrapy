# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-14

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class TaiChenInvestSpider(GGFundNavSpider):
    name = 'FundNav_TaiChenInvest'
    sitename = '泰诚资本'
    channel = '投顾净值'

    username = '350402197902120017'
    password = 'ZYYXSM123'
    fps = [{'url': 'http://www.taichengziben.com/tczb/index.php?m=product&a=index'}]

    def start_requests(self):
        yield FormRequest(url='http://www.taichengziben.com/tczb/index.php?m=login&a=index',
                          formdata={
                              'username': self.username,
                              'password': self.password
                          })

    def parse_fund(self, response):
        href_list = response.css('div#val_bottom a::attr(href)').extract()
        for href in href_list:
            self.ips.append({
                'url': 'http://www.taichengziben.com' + href,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath('//dl[@class="weizhi"]/dd/text()').extract_first()
        date_reg = re.findall('categories: \[(.*)\].*labels', response.text, re.DOTALL)[0]
        nav_reg = re.findall("基金净值走势.*data\s*:\s*\[(.*)\],.*'沪深300'", response.text, re.DOTALL)[0]
        date_list = [_.strip().replace('"', '') for _ in date_reg.split(',')]
        nav_list = [_.strip() for _ in nav_reg.split(',')]

        for date, nav in zip(date_list, nav_list):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav else None
            item['statistic_date'] = datetime.strptime(date, '%Y.%m.%d')
            yield item
