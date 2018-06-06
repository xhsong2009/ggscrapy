# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class PingAnXinTuoTrustSpider(GGFundNavSpider):
    name = 'FundNav_PingAnXinTuoTrust'
    sitename = '平安信托'
    channel = '信托净值'
    allowed_domains = ['trust.pingan.com']

    fps = [{'url': 'http://trust.pingan.com/products/1'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//tr//@href").extract()
        if fund_urls:
            for fund_url in fund_urls:
                self.ips.append({
                    'url': urljoin('http://trust.pingan.com', fund_url),
                    'ref': response.url,
                })
        next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url:
            self.fps.append({
                'url': urljoin('http://trust.pingan.com', str(next_url)),
                'ref': response.url,
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='table-body']/table/tbody//tr")
        fund_name = response.xpath("//h2[@class='product-name']//text()").extract_first()
        for row in rows:
            statistic_date = row.xpath("./td[1]//text()").extract_first().strip()

            if '2' in statistic_date:
                nav = row.xpath("./td[2]//text()").extract_first().strip()
                added_nav = row.xpath("./td[3]//text()").extract_first().strip()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                yield item
