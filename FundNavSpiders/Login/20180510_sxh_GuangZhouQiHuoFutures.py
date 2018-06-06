# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-10

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class GuangZhouQiHuoFuturesSpider(GGFundNavSpider):
    name = 'FundNav_GuangZhouQiHuoFutures'
    sitename = '广州期货'
    channel = '期货净值'
    allowed_domains = ['www.gzf2010.com.cn']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'UM_distinctid=162dcfa8c9c10d-0fd046460da28a-3c604504-15f900-162dcfa8c9d40a; yunsuo_session_verify=f5fe86d4185ef28b5bea1a33951efe74; ASP.NET_SessionId=fujnrtj2ec1tdk55iykd2n55; Bs_SessionID=201805100937164687; CNZZDATA1254886268=1712538512-1524123062-%7C1525912206; UserInfo=13352'

    fps = [
        {'url': 'https://www.gzf2010.com.cn/product.aspx?c=01&page=1', 'pg': 1},
        {'url': 'https://www.gzf2010.com.cn/product.aspx?c=02&page=1', 'pg': 1},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='r right right_all']/div[@class='box']/p[@class='p1']//a")
        if fund_urls:
            for url in fund_urls:
                fund_url = url.xpath('./@href').extract_first()
                fund_name = url.xpath('./text()').extract_first()
                self.ips.append({
                    'url': 'https://www.gzf2010.com.cn/table.aspx?' + fund_url.replace('Showpro.aspx?', '') + '&page=1',
                    'ref': response.url,
                    'ext': {'fund_name': fund_name},
                    'pg': 1
                })
            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('&page=' + str(pg), '&page=' + str(next_pg))
            self.fps.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,

            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//tr")
        for row in rows[1:]:
            statistic_date = row.xpath("./td[1]//text()").extract_first()
            nav = row.xpath("./td[2]//text()").extract_first()
            added_nav = row.xpath("./td[3]//text()").extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        if len(rows) > 1:
            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('&page=' + str(pg), '&page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name},
            })

