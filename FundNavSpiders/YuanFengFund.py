# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YuanFengFundSpider(GGFundNavSpider):
    name = 'FundNav_YuanFengFund'
    sitename = '源沣资本'
    channel = '投顾净值'

    cookies = 'hlk=checkboxs=1&ty=123'

    fps = [
        {
            'url': 'http://www.yffund.com.cn/product.asp',
            'ref': None
        }
    ]

    def parse_fund(self, response):
        rows = response.xpath('//table/tr/td[1]/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@id="tabs4_con_2"]/table/tr')[1:]
        for row in rows:
            fund_name = row.xpath('./td[1]/text()').extract_first()
            nav = row.xpath('./td[2]/text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[3]/text()').re_first('[0-9.]+')
            statistic_date = row.xpath('./td[7]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
