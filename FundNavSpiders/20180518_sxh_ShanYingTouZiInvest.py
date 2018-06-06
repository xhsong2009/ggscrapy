# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShanYingTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShanYingTouZiInvest'
    sitename = '善盈投资'
    channel = '投资顾问'
    allowed_domains = ['www.sying.cc']

    fps = [{'url': 'http://www.sying.cc/f/product/2#SYFund'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='SY-funds']//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.sying.cc' + fund_url,
                'ref': response.url,
                'pg': 1
            })

    def parse_item(self, response):
        fund_name = response.xpath("//div[@class='SY-invent']/h1//text()").extract_first()
        rows = response.xpath("//div[@class='body']/table[@id='fundValueTable']//tr")
        for row in rows:
            statistic_date = row.xpath("./td[1]//text()").extract_first()
            nav = row.xpath("./td[2]//text()").extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y.%m.%d')
            yield item
