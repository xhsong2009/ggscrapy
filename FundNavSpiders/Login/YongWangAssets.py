# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YongWangAssetsSpider(GGFundNavSpider):
    name = 'FundNav_YongWangAssets'
    sitename = '永望资产'
    channel = '投资顾问'

    username = '123'
    password = '123456'
    fps = [{
        'url': 'http://www.ywasset.com/product/index.php?c=show&id=1'
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.ywasset.com/member/index.php?c=login&m=index',
                          formdata={
                              'back': '',
                              'data[username]': self.username,
                              'data[password]': self.password
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        url = response.xpath('//div[@id="messagetext"]/p/script/@src').extract_first()
        yield Request(url=urljoin(get_base_url(response), url),
                      )

    def parse_fund(self, response):
        funds = response.xpath("//div[@class='fl pagleft']/ul/li/a")
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
        rows = response.xpath('//table/tbody/tr')[1:]
        for row in rows:
            statistic_date = row.xpath('./td[1]//text()').re_first('\d+/\d+/\d+')
            nav = row.xpath('./td[2]//text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[3]//text()').re_first('[0-9.]+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
            yield item
