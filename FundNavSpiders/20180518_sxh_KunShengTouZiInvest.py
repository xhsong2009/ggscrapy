# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class KunShengTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_KunShengTouZiInvest'
    sitename = '坤盛投资'
    channel = '投资顾问'
    allowed_domains = ['www.ntkstz.com']

    ips = [{'url': 'http://www.ntkstz.com/index.asp'}]

    def parse_item(self, response):
        rows = response.xpath("//div/div/table//tr")
        fund_names = response.xpath("//div/p/b//text()").extract()
        fund_name = ''.join(fund_names)
        for row in rows[1:]:
            nav = row.xpath('./td[1]/p//text()').extract()[1]
            added_nav = row.xpath('./td[2]/p//text()').extract()[1]
            statistic_date = row.xpath('./td[3]/p//text()').extract()[1]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name.replace('净值表', '')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y.%m.%d')
            yield item
