# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-04

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class ZiTanAssetSpider(GGFundNavSpider):
    name = 'FundNav_ZiTanAsset'
    sitename = '杭州紫潭投资'
    channel = '投顾净值'

    fps = [{
        'url': 'http://zt-assets.idc.gszwz.cn/list-90-1.html'
    }]

    def parse_fund(self, response):
        fund_href_list = response.xpath('//div[@class="submenu "]/div[@class="subNavBox"]/ul/li/a//@href').extract()
        for href in fund_href_list:
            url = 'http://zt-assets.idc.gszwz.cn/' + href
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        nav_list = response.xpath("//div[@class='main']//ul[2]//tr")
        fund_name_list = response.xpath("//div[@class='cont']/h2")
        fund_name = fund_name_list.xpath('.//text()').extract_first()
        for row in nav_list[1:]:
            i = row.xpath(".//text()").extract()
            i2 = [_ for _ in i if _.strip()]
            statistic_date = i2[0]
            nav = i2[1]
            added_nav = i2[2]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y.%m.%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

