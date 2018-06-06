# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-04-27

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HangZhouDeRuiZiBenTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HangZhouDeRuiZiBenTouZiInvest'
    sitename = '杭州德锐资本投资'
    channel = '投资顾问'

    fps = [{'url': 'http://www.winner98.net/yejizhanshi/id-1.html'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("///div[@class='acc-box']/a")
        for url in fund_urls:
            fund_url = url.xpath("./@href").extract_first()
            fund_name = url.xpath(".//text()").extract_first()
            self.ips.append({
                'url': 'http://www.winner98.net/?a=ajax&mod=' + fund_url.replace('/', '').replace('id-',
                                                                                                  '&id=').replace(
                    '.html', '&page=1'),
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//tr")
        if len(rows) > 1:
            for row in rows[1:]:
                statistic_date = row.xpath("./td[2]//text()").extract_first()
                nav = row.xpath("./td[3]//text()").extract_first().replace('\\u5143","page":"', '').replace('\\u5143',
                                                                                                            '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('&page=' + str(pg), '&page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })

