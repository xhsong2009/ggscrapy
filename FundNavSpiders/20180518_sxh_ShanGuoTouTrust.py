# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class ShanGuoTouTrustSpider(GGFundNavSpider):
    name = 'FundNav_ShanGuoTouTrust'
    sitename = '陕国投'
    channel = '信托净值'
    allowed_domains = ['www.siti.com.cn']

    fps = [
        {'url': 'http://www.siti.com.cn/product.php?fid=23&fup=3&pageid=1',
         'pg': 1},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='proDl']//tr//@href").extract()
        for fund_url in fund_urls:
            fund_pg = re.findall('pageid=(\d+)', fund_url)[0]
            self.ips.append({
                'url': 'http://www.siti.com.cn/' + fund_url.replace('pageid=' + fund_pg, 'pageid=1'),
                'ref': response.url,
                'pg': 1
            })

        if fund_urls:
            pg = response.meta['pg']
            next_pg = pg + 1
            self.fps.append({
                'url': 'http://www.siti.com.cn/product.php?fid=23&fup=3&pageid=' + str(next_pg),
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        fund_name = response.xpath("//div[@class='proTitle'][1]/h1//text()").extract_first()
        rows = response.xpath("//div[@class='proDl']//tr")
        if len(rows) > 1:
            for row in rows[1:]:
                statistic_date = row.xpath("./td[1]//text()").extract_first().replace('年', '-').replace('月',
                                                                                                        '-').replace(
                    '日', '')
                nav = row.xpath("./td[3]").re_first('>\s*([0-9.]+)\s*<')
                added_nav = row.xpath("./td[4]").re_first('>\s*([0-9.]+)\s*<')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            pg = response.meta['pg']
            next_pg = pg + 1
            self.ips.append({
                'url': response.url.replace('pageid=' + str(pg), 'pageid=' + str(next_pg)),
                'ref': response.url,
                'pg': next_pg,
            })
