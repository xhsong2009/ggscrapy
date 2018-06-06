# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhongGangFuturesSpider(GGFundNavSpider):
    name = 'FundNav_ZhongGangFutures'
    sitename = '中钢期货'
    channel = '期货净值'

    fps = [
        {
            'url': 'http://www.zgfcc.com/zhonggang/tbzl7.aspx?id=236&idl=0&ex=3&yjml=236&ejml='
        }
    ]

    def parse_fund(self, response):
        rows = response.xpath('//table/tr/td/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//tbody/tr')[1:] if response.xpath('//tbody/tr[1]/td[1]/text()').extract_first().strip() == '产品名称' else response.xpath('//table/tbody/tr/td[1]/table/tbody/tr')[1:]
        for row in rows:
            fund_name = row.xpath('./td[1]/text()').extract_first().strip()
            statistic_date = row.xpath('./td[2]/text()').re_first('\d+/\d+/\d+')
            nav = row.xpath('./td[3]/text()').re_first('[0-9.]+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
            yield item
