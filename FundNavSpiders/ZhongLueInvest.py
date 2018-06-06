# -*- coding: utf-8 -*-

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import re


class ZhongLueInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZhongLueInvest'
    sitename = '厦门中略投资管理有限公司'
    channel = '投顾净值'

    fps = [{
        'url': 'http://www.zhongluefund.com/products.aspx?productsCateID=78&products_Id=78&CateId=78&ViewCateID=78',
        'ref': 'http://www.zhongluefund.com/'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//div[@class="menu_1"]/a')
        for fund in funds:
            id = fund.xpath("./@href").extract_first()
            fund_name = fund.xpath("./text()").extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), id),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="w100"]/table/tbody/tr')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            statistic_date = row.xpath('normalize-space(./td[1]/text())').extract_first()
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = row.xpath('normalize-space(./td[2]/text())').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = statistic_date
            item['nav'] = float(nav) if nav is not None else None

            yield item
        dates = re.search('categories:\s*\[([^\]]+)\]\s*\},', response.text).group(1)
        dates = re.findall('\d+-\d+-\d+', dates)
        added_navs = re.search("name:\s*'累计净值',\s*data:\s*\[([^\]]+)\]", response.text).group(1)
        added_navs = re.findall('[0-9.]+', added_navs)
        for date, added_nav in zip(dates, added_navs):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = date
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            added_nav = added_nav
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item