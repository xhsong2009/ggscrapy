# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LingZhenZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_LingZhenZiChanInvest'
    sitename = '领真资产'
    channel = '投资顾问'
    allowed_domains = ['www.lzasset.com']

    fps = [{'url': 'http://www.lzasset.com/funds.php?ntc=1'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='fund_list']//a")
        for url in fund_urls:
            fund_url = url.xpath(".//@href").extract_first()
            fund_name = url.xpath(".//text()").extract_first()
            if fund_url:
                self.ips.append({
                    'url': 'http://www.lzasset.com' + fund_url + '&page=1&ntc=1',
                    'ref': response.url,
                    'ext': {'fund_name': fund_name,'last_one_date':""},
                    'pg': 1
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//div[@class='right_colume']//ul")
        if len(rows) > 1:
            for row in rows[1:]:
                statistic_date = row.xpath("./li[1]//text()").extract_first()
                nav = row.xpath("./li[2]//text()").extract_first()
                added_nav = row.xpath("./li[3]//text()").extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

            pg = response.meta['pg']
            last_two_date = response.meta['ext']['last_one_date']
            last_one_date = statistic_date
            if last_one_date != last_two_date:
                next_pg = pg + 1
                next_url = response.url.replace('page=' + str(pg), 'page=' + str(next_pg))
                self.ips.append({
                    'url': next_url,
                    'ref': response.url,
                    'pg': next_pg,
                    'ext': {'fund_name': fund_name,'last_one_date':last_one_date}
                })

