# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class HaoEnTouZiSpider(GGFundNavSpider):
    name = 'FundNav_HaoEnTouZi'
    sitename = '昊恩投资'
    channel = '投资顾问'
    allowed_domains = ['www.hetz.com.cn']

    ips = [
        {'url': 'http://www.hetz.com.cn/index.asp', },
    ]

    def parse_item(self, response):
        fund_names = re.findall('<OPTION VALUE="(\d+)(.*?)>(.*?)</OPTION>', response.text)
        for name in fund_names:
            fund_id = name[0]
            fund_name = name[2]
            zz = "//div[@id='d%s']//tr" % (fund_id)
            rows = response.xpath(zz)
            for row in rows[1:]:
                nav = row.xpath('./td[2]//text()').extract_first()
                statistic_date = row.xpath('./td[3]//text()').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y.%m.%d')
                item['nav'] = float(nav) if nav is not None else None

                yield item
