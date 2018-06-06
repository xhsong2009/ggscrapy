# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class DongFangZhengQuanChuangXinTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_DongFangZhengQuanChuangXinTouZiInvest'
    sitename = '上海东方证券创新投资'
    channel = '投资顾问'
    allowed_domains = ['dzcx.dfzq.com.cn']
    ips = [
        {'url': 'http://dzcx.dfzq.com.cn/js/product.js'},
    ]

    def parse_item(self, response):
        fund_names = re.findall('"name" : "(.*?)",', response.text)
        navs = re.findall('"unit" : "(.*?)",', response.text)
        added_navs = re.findall('"accumulation" : "(.*?)",', response.text)
        statistic_dates = re.findall('"date" : "(.*?)"', response.text)
        for row in zip(fund_names, statistic_dates, navs, added_navs):
            fund_name = row[0]
            statistic_date = row[1]
            nav = row[2]
            added_nav = row[3]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
            yield item
