# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-07

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class XunShiFundSpider(GGFundNavSpider):
    name = 'FundNav_XunShiFund'
    sitename = '青岛循实投资'
    channel = '投资顾问'

    fps = [{'url': 'http://www.xunshifund.com/zhaoshang.asp?id=63'}]

    def parse_fund(self, response):
        fund_urls = response.xpath('//div[@class="mian_nav"]/ul/li[4]/a/@href').extract()
        fund_name = response.xpath('//div[@class="neiy_main"]//div/div[2]/ul/li[1]//text()').extract()
        for url, name in zip(fund_urls, fund_name):
            ips_url = urljoin('http://www.xunshifund.com/default.asp', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//div[@class="form_table"]/table/tbody//tr')
        for row in rows[1:]:
            fund_date = row.xpath('.//td[1]//text()').extract_first()
            added_nav = row.xpath('.//td[2]//text()').extract_first()
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y年%m月%d日')
            item['added_nav'] = float(added_nav)
            yield item
