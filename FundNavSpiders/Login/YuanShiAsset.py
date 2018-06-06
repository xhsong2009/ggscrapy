# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YuanShiAssetSpider(GGFundNavSpider):
    name = 'FundNav_YuanShiAsset'
    sitename = '源实资产'
    channel = '投顾净值'
    allowed_domains = ['http://www.jvam.com.cn/index.php']

    cookies = 'PHPSESSID=fvvj839qqn7turu71h08rbhmt5'  # cookie固定
    username = '18602199319'
    password = 'yadan0319'

    def start_requests(self):
        yield Request(url='http://www.jvam.com.cn/products', callback=self.parse_login)

    def parse_login(self, response):
        urls = response.xpath('//ul[@class="pl-ul"]/li/ul/li/a/@href').extract()
        for url in urls:
            self.fps.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_fund(self, response):
        fund_name = response.xpath('normalize-space(//div[@id="pr-info"]/table/tr[1]/td[2]/text())').extract_first()
        self.ips = [{
            'url': response.url.replace('info', 'data') + '?p=1',
            'ref': response.url,
            'pg': 1,
            'ext': {'fund_name': fund_name}
        }]

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//tr')
        if len(rows) != 0:
            for row in rows:
                nav = row.xpath('./td[1]/text()').extract_first()
                added_nav = row.xpath('./td[2]/text()').extract_first()
                statistic_date = row.xpath('./td[4]/text()').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('?p=' + str(pg), '?p=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })
