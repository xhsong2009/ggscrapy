# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class FengYiTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_FengYiTouZiInvest'
    sitename = '上海沣谊投资'
    channel = '投资顾问'
    allowed_domains = ['www.blossomfund.cn']

    fps = [
        {'url': 'http://www.blossomfund.cn/product/index'},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='left']//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.blossomfund.cn' + fund_url + '&page=1',
                'ref': response.url,
                'pg': 1
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='right']//tr")
        for row in rows[1:]:
            fund_name = row.xpath("./td[1]//text()").extract_first()
            statistic_date = row.xpath("./td[4]//text()").extract_first()
            nav = row.xpath("./td[2]//text()").extract_first().replace('(', '（').split('（')[0]
            added_nav = row.xpath("./td[3]//text()").extract_first().replace('(', '（').split('（')[0]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            if fund_name == '沣谊一号':
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav_2'] = float(added_nav) if added_nav is not None else None
            else:
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
