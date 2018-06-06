# -*- coding: utf-8 -*-
# Department：保障部
# Author：王卓诚
# Create_Date：2018-05-28

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class JinDeZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_JinDeZiChanInvest'
    sitename = '金锝资产'
    channel = '投顾净值'
    allowed_domains = ['www.jindefund.com']

    fps = [{'url': 'http://www.jindefund.com/page.aspx?node=12'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='pz_SideLayer']/li")
        for url in fund_urls:
            fund_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first()
            self.ips.append({
                'url': 'http://www.jindefund.com' + fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='t_240']/ul/li")
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            statistic_date = row.xpath("./div[1]//text()").extract_first()
            nav = row.xpath("./div[2]//text()").extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
