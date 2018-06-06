# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-17


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShangHaiYingZhiAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiYingZhiAsset'
    sitename = '上海应治资产'
    channel = '投资顾问'
    allowed_domains = ['www.zenithmacer.com']

    fps = [
        {'url': 'http://www.zenithmacer.com/c/l-143-0.html'},
        {'url': 'http://www.zenithmacer.com/c/l-141-0.html'},
        {'url': 'http://www.zenithmacer.com/c/l-138-0.html'},
    ]

    def parse_fund(self, response):
        funds = response.xpath('//h2//a//@href').extract()
        for f_url in funds:
            fund_url = 'http://www.zenithmacer.com' + f_url
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
            })

    def parse_item(self, response):
        funds_list = response.xpath('//table//tr')
        for i in funds_list[1:]:
            t = i.xpath('td//text()').extract()
            fund_name = ''.join(t[0].split())
            statistic_date = ''.join(t[1].split())
            nav = ''.join(t[2].split())
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
            item['nav'] = float(nav) if nav is not None else None
            yield item
