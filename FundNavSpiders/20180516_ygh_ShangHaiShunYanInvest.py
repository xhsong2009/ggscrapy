# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-16


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShangHaiShunYanInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiShunYanInvest'
    sitename = '上海顺彦投资'
    channel = '投资顾问'
    allowed_domains = ['www.shunyanjijin.com']

    ips = [{
        'url': 'http://www.shunyanjijin.com/nianshouyilv/',
    }]

    def parse_item(self, response):
        f_list = response.xpath('//table//tbody[@bgcolor ="#ffffff"]//tr')
        for i in f_list:
            item = GGFundNavItem()
            t = i.xpath('td//text()').extract()
            fund_name = t[0]
            nav = t[4]
            statistic_date = t[6]
            item['nav'] = float(nav) if nav is not None else None
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date,'%Y/%m/%d')
            yield item



