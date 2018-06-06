# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-18


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request


class ShangHaiShiHuiAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiShiHuiAsset'
    sitename = '上海拾晖资产'
    channel = '投资顾问'
    allowed_domains = ['www.shihuizc.com']

    def start_requests(self):
        yield Request(url='http://www.shihuizc.com/index.php?ac=article&at=list&tid=8',
                          callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        funds_urls = response.xpath('//div[@class = "prod_divs"]//@onclick').extract()
        for funds_url in funds_urls:
            self.fps.append({
                'url': 'http://www.shihuizc.com/index.php?' + funds_url.split('?')[1],
            })

    def parse_fund(self, response):
        funds = response.xpath('//ul[@class ="menu"]//li//a//@href').extract()
        fund_names = response.xpath('//ul[@class ="menu"]//li//a//text()').extract()
        for fund_name, f_url in zip(fund_names, funds):
            self.ips.append({
                'url': f_url,
                'ref': response.url,
                'ext': fund_name if '产品' not in fund_name else None
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        f_list = response.xpath('//table//tr')
        for i in f_list[1:]:
            t = i.xpath('td//text()').extract()
            statistic_date = t[1]
            nav = t[2]
            added_nav = t[3]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date,
                                                       '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            yield item
