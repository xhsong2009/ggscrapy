# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-22

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class YiYuanXinFundSpider(GGFundNavSpider):
    name = 'FundNav_YiYuanXinFund'
    sitename = '江苏易元鑫资产'
    channel = '投顾净值'
    allowed_domains = ['www.eyxfund.com']

    username = '13461073668'
    password = '123456'

    fps = [{'url': 'http://www.eyxfund.com/Product'}]
    cookies = 'ASP.NET_SessionId=ekybn1kobru4x5s0ujugime0; xjly=hayden'

    def parse_fund(self, response):
        link = response.xpath('//div[@id="item_content1"]//li//@href').extract()
        for link_key in link:
            if link_key not in 'javascript:void(0);':
                href = link_key
                ips_url = urljoin('http://www.eyxfund.com', href)
                self.ips.append({
                    'url': ips_url,
                    'ref': response.url,
                })

    def parse_item(self, response):
        fund_name_list = response.xpath('//div[@class="item_div1"]/div/h1')
        fund_name = fund_name_list.xpath('.//text()').extract_first()
        if fund_name:
            row = response.xpath('////div[@class="coop_namej"]/table/tbody/tr')
            for rows in row[1:]:
                nav_list = rows.xpath('td//text()').extract()
                statistic_date = nav_list[0]
                nav = nav_list[1].replace(' ', '')
                added_nav = nav_list[2].replace(' ', '')

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item
