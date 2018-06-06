# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class HengJiangUnionSpider(GGFundNavSpider):
    name = 'FundNav_HengJiangUnion'
    sitename = '前海恒江联合'
    channel = '投顾净值'
    allowed_domains = ['hjlhtz.com']
    fps = [{'url': 'http://hjlhtz.com/notice.htm?id=1'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@id='pro_nav_content']/div/div/div//a")
        for url in fund_urls:
            fund_url = url.xpath('.//@href').extract_first()
            ips_url = urljoin('http://hjlhtz.com/products.htm', fund_url)
            fund_name = url.xpath('.//text()').extract_first()
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//table//tr")
        for row in rows[1:]:
            fund_date = row.xpath('.//td[1]//text()').extract_first()
            nav = row.xpath('.//td[2]//text()').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y%m%d')
            item['nav'] = float(nav)
            yield item
