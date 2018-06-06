# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-10


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShangHaiJingXiangAssetsSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiJingXiangAssets'
    sitename = '上海鲸象资产'
    channel = '投顾净值'
    allowed_domains = ['www.jxassets.com']

    fps = [{'url': 'http://www.jxassets.com/fund.html'}]

    def parse_fund(self, response):
        fund_urls = response.xpath('//ul[@id ="treeNav"]//a//@href').extract()
        for url in fund_urls:
            self.ips.append({
                'url': 'http://www.jxassets.com/' + url,
                'ref': response.url,
            })

    def parse_item(self, response):
        fund = response.xpath('//table[@id = "table"]//tr')
        for i in fund[1:]:
            t = i.xpath('td//text()').extract()
            item = GGFundNavItem()
            fund_name = t[0]
            statistic_date = t[2]
            nav = t[4]
            added_nav = t[5]
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            yield item
