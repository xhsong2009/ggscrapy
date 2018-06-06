# -*- coding: utf-8 -*-

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class UsuFundSpider(GGFundNavSpider):
    name = 'FundNav_UsuFund'
    sitename = '优素资产'
    channel = '投资顾问'
    # 入口地址
    start_urls = ['http://www.usufund.com/']

    cookies = 'UM_distinctid=163203b5378301-0f634f77a34da2-3f3c5701-15f900-163203b537917a; JSESSIONID=AF437CE550F5C3531DB357ED714C6FFD; SESSION=93b1d228-f95b-4e2e-9510-46f7758c65b6; CNZZDATA1259878002=1137005077-1525253551-http%253A%252F%252Finfo.hffss.com%252F%7C1527042591'

    fps = [
        {
            'url': 'http://info.hffss.com/app/reg/show',
            'ref': 'http://info.hffss.com/app/reg/show'
        }
    ]

    def parse_fund(self, response):

        funds = response.css('.am-accordion-content>div>div:nth-child(2)')
        for fund in funds:
            fund_name = fund.xpath('./div[@class="pro-name"]/text()').extract_first()
            pid = fund.xpath('./input[@class="pidInput"]/@value').extract_first()
            self.ips.append({
                'url': 'http://info.hffss.com/app/prosummary/' + pid,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        rows = response.xpath("//input[@id='nv12m']/@value").extract_first()
        rows = eval(rows)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row[0]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row[2]
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row[3]
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

