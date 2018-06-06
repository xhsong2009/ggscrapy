# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LingRiZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_LingRiZiChanInvest'
    sitename = '凌日资产'
    channel = '投资顾问'
    allowed_domains = ['www.lrfunds.com']

    fps = [{'url': 'http://www.lrfunds.com/products/47-7.html'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@id='side_list']/ul/li")
        for url in fund_urls:
            fund_url = url.xpath(".//@href").extract_first()
            fund_name = url.xpath(".//text()").extract_first()
            if fund_url:
                self.ips.append({
                    'url': 'http://www.lrfunds.com' + fund_url.replace('.html', '_1.html'),
                    'ref': response.url,
                    'ext': {'fund_name': fund_name},
                    'pg': 1
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//table[@class='jingzhi']//tr")
        if rows:
            for row in rows:
                statistic_date = row.xpath("./td[1]//text()").extract_first()
                nav = row.xpath('./td[2]//text()').extract_first()
                added_nav = row.xpath('./td[3]//text()').extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                if added_nav:
                    item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                yield item

            pg = response.meta['pg']
            next_pg = pg + 1
            next_url = response.url.replace('_' + str(pg) + '.html', '_' + str(next_pg) + '.html')
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })
