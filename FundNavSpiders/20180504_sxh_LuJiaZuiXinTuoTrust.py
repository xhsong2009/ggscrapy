# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LuJiaZuiXinTuoTrustSpider(GGFundNavSpider):
    name = 'FundNav_LuJiaZuiXinTuoTrust'
    sitename = '陆家嘴信托'
    channel = '信托净值'
    allowed_domains = ['www.ljzitc.com.cn']

    fps = [{'url': 'http://www.ljzitc.com.cn/news/cpjzsy/index.html'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='wrap div100 mb10']//a")
        for url in fund_urls:
            fund_url = url.xpath(".//@href").extract_first()
            fund_name = url.xpath("./div[@class='pro_left width40 FL text_l']//text()").extract_first()
            if fund_url:
                self.ips.append({
                    'url': 'http://www.ljzitc.com.cn' + fund_url,
                    'ref': response.url,
                    'ext': {'fund_name': fund_name},
                    'pg': 1
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//div[@class='contant_productcon']//tr")
        for row in rows[1:]:
            statistic_date = row.xpath("./td[1]//text()").extract_first()
            nav = row.xpath("./td[2]//text()").extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
