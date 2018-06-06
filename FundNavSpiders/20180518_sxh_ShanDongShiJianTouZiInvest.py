# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18
# Alter_Date : 2018-05-24

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import calendar


class ShanDongShiJianTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShanDongShiJianTouZiInvest'
    sitename = '山东时间投资'
    channel = '投资顾问'
    allowed_domains = ['www.timefund.cn']
    ips = [
        {'url': 'http://www.timefund.cn/a/fuwuyuchanpin/guonawuliu/'},
    ]

    def parse_item(self, response):
        fund_name = re.findall("name:'(.*?)',", response.text)[0]
        navs = re.findall('var chanpinjingzhi = \[(.*?)\];', response.text)[0].replace(' ', '').split(',')
        statistic_dates = re.findall("var times =        \[(.*?)\];",
                                     response.text)[0].replace(' ', '').replace("'", '').split(",")
        for row in zip(statistic_dates, navs):
            nav = row[1]
            date = row[0].replace('.', '-')
            if len(date) < 8:
                year = int(date[0:4])
                month = int(date[5:])
                wday, monthrange = calendar.monthrange(year, month)
                weekday = calendar.weekday(year, month, monthrange)
                if weekday == 5:
                    monthrange = monthrange - 1
                elif weekday == 6:
                    monthrange = monthrange - 2
                statistic_date = date + '-' + str(monthrange)
            else:
                statistic_date = date
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        fund_name1 = re.findall("name:'(.*?)',", response.text)[2]
        navs1 = re.findall('var sachina = \[(.*?)\];', response.text)[0].replace(' ', '').split(',')
        statistic_dates1 = re.findall("var sachinaTimes = \[(.*?)\];",
                                      response.text)[0].replace(' ', '').replace("'", '').split(",")
        for row1 in zip(statistic_dates1, navs1):
            nav1 = row1[1]
            date1 = row1[0].replace('.', '-')
            if len(date1) < 8:
                year1 = int(date1[0:4])
                month1 = int(date1[5:])
                wday1, monthrange1 = calendar.monthrange(year1, month1)
                weekday1 = calendar.weekday(year1, month1, monthrange1)
                if weekday1 == 5:
                    monthrange1 = monthrange1 - 1
                elif weekday1 == 6:
                    monthrange1 = monthrange1 - 2
                statistic_date1 = date1 + '-' + str(monthrange1)
            else:
                statistic_date1 = date1

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name1
            item['nav'] = float(nav1) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date1, '%Y-%m-%d')
            yield item
