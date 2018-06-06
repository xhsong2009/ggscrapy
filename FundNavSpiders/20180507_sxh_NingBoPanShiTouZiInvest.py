# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-07

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request


class NingBoPanShiTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_NingBoPanShiTouZiInvest'
    sitename = '宁波磐石投资'
    channel = '投顾净值'
    allowed_domains = ['www.nbpstz.com/']

    def start_requests(self):
        yield Request(url='http://www.nbpstz.com/web/index.php?s=/Fund/index.html',
                      callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        fund_urls = response.xpath("//div[@class='bg']")
        for url in fund_urls:
            fund_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first()
            self.fps.append({
                'url': 'http://www.panshifund.com' + fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_fund(self, response):
        fund_url = response.xpath("//a[contains(., '点击详情了解')]//@href").extract_first()
        fund_name = response.meta['ext']['fund_name']
        if fund_url:
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@id='jj']//tr")
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            statistic_date = row.xpath("./td[4]//text()").extract_first().strip()
            added_nav = row.xpath("./td[3]//text()").extract_first().strip()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

