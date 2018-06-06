# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class TianBeiHeZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_TianBeiHeZiChanInvest'
    sitename = '广东天贝合资产'
    channel = '投资顾问'
    allowed_domains = ['www.ten-bagger.com']
    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.ten-bagger.com/zh-CN/products.php?page=1'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//table[2]//table//table//table[1]//tr")
        for url in fund_urls:
            fund_url = url.xpath("./td//@href").extract_first()
            fund_name = url.xpath("./td//text()").extract_first()
            if fund_url and 'displayproduct' in fund_url:
                self.ips.append({
                    'url': 'http://www.ten-bagger.com/zh-CN/' + fund_url,
                    'ref': response.url,
                    'ext': {'fund_name': fund_name},
                })
        if len(fund_urls) > 5:
            pg = response.url.replace('http://www.ten-bagger.com/zh-CN/products.php?page=', '')
            next_pg = str(int(pg) + 1)
            self.fps.append({
                'url': response.url.replace('?page=' + pg, '?page=' + next_pg),
                'ref': response.url,

            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//div[@class='c02_content']/table[@class='product']/tbody//tr")
        for row in rows[1:]:
            statistic_date = row.xpath("./td[2]//text()").extract_first()
            nav = row.xpath('./td[3]//text()').extract_first()
            added_nav = row.xpath('./td[4]//text()').extract_first()
            if '2' in statistic_date:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item


