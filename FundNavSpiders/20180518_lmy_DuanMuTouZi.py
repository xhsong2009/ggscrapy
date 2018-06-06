# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class DuanMuTouZiSpider(GGFundNavSpider):
    name = 'FundNav_DuanMuTouZi'
    sitename = '四川端木投资'
    channel = '投资顾问'
    allowed_domains = ['www.duanmutouzi.com']

    ips = [
        {'url': 'http://www.duanmutouzi.com/home.html'}
    ]

    def parse_item(self, response):
        rows = response.xpath("//div[@class='hca_pro fl']//tr")
        for row in rows[1:]:
            i = row.xpath("./td//text()").extract()
            if i[2] not in '已结束':
                fund_name = i[0]
                statistic_date = i[3]
                nav = i[2]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None

                yield item
