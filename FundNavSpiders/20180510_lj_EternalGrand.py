# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-10

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class EtenalGrandSpider(GGFundNavSpider):
    name = 'FundNav_EtenalGrand'
    sitename = '深圳恒泰融安投资'
    channel = '投顾净值'
    allowed_domains = ['www.eternalgrand.com']
    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = '__guid=88917149.2507931099894912000.1525935285317.8052; monitor_count=15',

    fps = [{'url': 'http://www.eternalgrand.com/fuwuxiangmu/jingzhipilu/'}]

    def parse_fund(self, response):
        href_list = response.xpath('//ul[@class="cppu-contant"]//li//@href').extract()
        fund_names = response.xpath('//ul[@class="cppu-contant"]//li/p[1]//text()').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.eternalgrand.com/fuwuxiangmu/jingzhipilu/', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="content"]/div/table//tr')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            fund_date = row.xpath('.//td[2]//text()').extract_first().strip()
            fund_nav = row.xpath('.//td[3]//text()').extract_first().strip()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y/%m/%d')
            item['nav'] = float(fund_nav)
            yield item

