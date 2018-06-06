# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class CapallAssetSpider(GGFundNavSpider):
    name = 'FundNav_CapallAsset'
    sitename = '开宝资产'
    channel = '投资顾问'

    fps = [{'url': 'http://www.capall.com.cn/',
            'ref': 'http://www.kindoasset.com/'}]

    def parse_fund(self, response):
        fund_infos = response.xpath('//div[@class="navbox"]/div/ul/li[5]/ul//li')
        for url in fund_infos:
            fund_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first()
            ips_url = urljoin('http://www.capall.com.cn/', fund_url)
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='skmain']/div[2]//tr")
        for row in rows[1:]:
            fund_name = row.xpath('.//td[1]//text()').extract_first()
            fund_date = row.xpath('.//td[5]//text()').extract_first()
            fund_nav = row.xpath('.//td[2]//text()').extract_first()
            if fund_nav:
                item = GGFundNavItem()

                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(fund_date.replace('.', '-'), '%Y-%m-%d')
                item['nav'] = float(fund_nav)
                yield item
