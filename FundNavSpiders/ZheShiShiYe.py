# coding:utf-8

from datetime import datetime
from urllib.parse import urljoin
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem
from scrapy.utils.response import get_base_url


class ZheShiShiYeSpider(GGFundNavSpider):
    name = 'FundNav_ZheShiShiYe'
    sitename = '哲实实业'
    channel = '投资顾问'

    fps = [
        {'url': 'http://www.zs9188.com/Value.aspx'}
    ]

    def parse_fund(self, response):
        funds = response.xpath('//ul[@class="left_nav"]/li/a')
        for fund in funds:
            url = fund.xpath("./@href").extract_first()
            ips_url = urljoin(get_base_url(response), url)
            fund_name = fund.xpath("./text()").extract_first()
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        funds = response.xpath('//tr')[1:]
        for fund in funds:
            nav = fund.xpath('./td[5]//span/text()').extract_first()
            added_nav = fund.xpath('./td[6]//span/text()').extract_first()
            statistic_date = fund.xpath('./td[3]//span/text()').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item
