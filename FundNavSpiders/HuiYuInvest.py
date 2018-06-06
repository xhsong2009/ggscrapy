# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HuiYuInvestSpider(GGFundNavSpider):
    name = 'FundNav_HuiYuInvest'
    sitename = '云南汇誉投资'
    channel = '投资顾问'

    fps = [
        {
            'url': 'http://www.huiyutouzi.cn/list.asp?id=6'
        }
    ]

    def parse_fund(self, response):
        rows = response.xpath('//div[@class="mm box1"]')[0].xpath('./ul/li/a[contains(text(),"产品历史净值")]')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath('//h1[@class="aTitle"]/text()').re_first('([^/]+)产品历史净值')
        rows = response.xpath('//table/tbody/tr')[1:]
        for row in rows:
            statistic_date = row.xpath('./td[1]//text()').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[2]//text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[3]//text()').re_first('[0-9.]+')

            if statistic_date is not None:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item
