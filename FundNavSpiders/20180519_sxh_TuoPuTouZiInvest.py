# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-19

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request


class TuoPuTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_TuoPuTouZiInvest'
    sitename = '拓璞投资'
    channel = '投顾净值'
    allowed_domains = ['www.top-investment.cn']

    ips = [
        {
            'url': 'http://www.top-investment.cn/product1.php?infoid=9&sid=12',
            'ext': {'fund_name': '万联拓璞1号'}
        },
    ]

    def start_requests(self):
        yield Request(
            url='http://www.top-investment.cn/product.php',
            callback=self.fund_list_name)

    def fund_list_name(self, response):
        fund_urls = response.xpath("//div[@class='container'][1]/table//tr/td[1]/table[2]//tr")
        for url in fund_urls:
            fund_name = url.xpath(".//text()").extract()[1]
            fund_url = url.xpath(".//@href").extract_first()
            if fund_url:
                self.fps.append({
                    'url': 'http://www.top-investment.cn/' + fund_url,
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })

    def parse_fund(self, response):
        fund_url = response.xpath("//a[contains(., '产品净值')]//@href").extract_first()
        fund_name = response.meta['ext']['fund_name']
        if fund_url:
            self.ips.append({
                'url': 'http://www.top-investment.cn/' + fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })
        else:
            self.ips.append({
                'url': response.url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='ff']//tr")
        fund_name = response.meta['ext']['fund_name']

        for row in rows:
            statistic_dates = row.xpath("./td[1]//text()").extract()
            statistic_date = ''.join(statistic_dates).replace('/', '-')
            nav = row.xpath("./td[2]//text()").extract_first()
            added_nav = row.xpath("./td[3]//text()").extract_first()
            if '20' in statistic_date:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
