# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YouYiFengAssetSpider(GGFundNavSpider):
    name = 'FundNav_YouYiFengAsset'
    sitename = '厦门祐益峰资产'
    channel = '投资顾问'

    cookies = 'PHPSESSID=acsfonglk7pmhbb71aldb283e0'  # cookie固定
    username = '820612602@qq.com'
    password = '123456'

    def start_requests(self):
        yield Request(url='http://www.youhillstock.com/index.php?m=Product&a=index', callback=self.parse_fund)

    def parse_fund(self, response):
        funds = response.xpath('//div[@class="subNav"]/ul/li/a')
        for fund in funds:
            url = fund.xpath('./@href').extract_first()
            fund_name = fund.xpath('./text()').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table[@id="dateTR"]/tbody/tr')
        for row in rows:
            nav = row.xpath('./td[2]/text()').extract_first()
            added_nav = row.xpath('./td[3]/text()').extract_first()
            statistic_date = row.xpath('./td[1]/text()').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            yield item

