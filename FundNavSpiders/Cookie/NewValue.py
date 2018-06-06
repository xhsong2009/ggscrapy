# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class NewValueSpider(GGFundNavSpider):
    name = 'FundNav_NewValue'
    sitename = '新价值'
    channel = '投顾净值'

    cookies = 'UM_distinctid=161bcc83bc04aa-0250cf6ddd829f-393d5f0e-15f900-161bcc83bc1195; ASPSESSIONIDACCBSQBT=BHFBIAACFCNNGACDAGNPFCLH; ASPSESSIONIDCCDASQAS=DJJNOOADOPEBOIJDEADGMGJO; ASPSESSIONIDAABATRBT=MHFDDFIAFIGLIPFLJCMOCEFJ; ASPSESSIONIDCACATRAS=LMDNABLAOJNLHAABDPHGLNEJ; ASPSESSIONIDCCCCRQBS=PBNLOIGAECEMJFHCPNFJLBNF; ASPSESSIONIDACDATRBT=EPODFEGAJNOEFPNPHNAHELDI; ASPSESSIONIDCASAQRTS=EJBPKBOCDFHKIDKLAFHMIKGJ; CNZZDATA2966838=cnzz_eid%3D535109687-1502961414-http%253A%252F%252Fwww.newvalue.com.cn%252F%26ntime%3D1527123493'

    username = '123456'
    password = '123456'

    def start_requests(self):
        yield Request(url='http://www.newvalue.com.cn/products.asp?pid=1', callback=self.parse_login)

    def parse_login(self, response):
        urls = response.xpath('//ul[@class="yiji"]/li/a/@href').extract()
        for url in urls:
            self.fps.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_fund(self, response):
        funds = response.xpath('//table[@class="pr_view"]/tr/td[1]/a')
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
        rows = response.xpath('//*[@id="group_one"]/tr')
        for row in rows:
            nav = row.xpath('./td[3]/text()').extract_first()
            statistic_date = row.xpath('./td[2]/text()').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            yield item

