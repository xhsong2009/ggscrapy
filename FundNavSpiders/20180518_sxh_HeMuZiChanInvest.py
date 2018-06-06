# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HeMuZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_HeMuZiChanInvest'
    sitename = '禾木资产'
    channel = '投资顾问'
    allowed_domains = ['www.hamcsz.com']

    ips = [{'url': 'http://www.hamcsz.com/index.asp'}]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="jz_content"]//tr')
        for row in rows:
            fund_name = row.xpath('./td[1]//text()').extract_first()
            nav = row.xpath('./td[2]//text()').extract_first()
            statistic_date = row.xpath('./td[3]//text()').extract_first().replace('.', '-')
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            yield item
