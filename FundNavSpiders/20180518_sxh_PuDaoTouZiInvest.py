# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class PuDaoTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_PuDaoTouZiInvest'
    sitename = '朴道投资'
    channel = '投顾净值'
    allowed_domains = ['www.pudaofund.com']

    fps = [
        {'url': 'http://www.pudaofund.com/product.do'},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='side sidePic_pro']/ul/li[@class='unselect']")
        for url in fund_urls:
            fund_name = url.xpath('.//text()').extract_first()
            fund_url = url.xpath('.//@href').extract_first()
            self.ips.append({
                'url': 'http://www.pudaofund.com' + fund_url.replace('.do', '_netvalue.do'),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='sub2Table']//tr")
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            statistic_date = row.xpath("./td[2]//text()").extract_first()
            nav = row.xpath("./td[3]//text()").extract_first()
            if nav:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
