# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-10

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy import FormRequest


class RiverInvestSpider(GGFundNavSpider):
    name = 'FundNav_RiverInvest'
    sitename = '深圳长流汇资产'
    channel = '投资顾问'
    allowed_domains = ['www.riverinvest.com.cn']
    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.riverinvest.com.cn/fsjj12.html'}]

    def start_requests(self):
        yield FormRequest(url='http://www.riverinvest.com.cn/login.asp',
                          formdata={'m_uid': 'ZYYXSM',
                                    'm_pwd': 'ZYYXSM123',
                                    'input_yzm': '',
                                    'action': 'login'}
                          )

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="aboutoutleft2"]/ul//li//@href').extract()
        fund_names = response.xpath('//div[@class="aboutoutleft2"]/ul//li//@title').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.riverinvest.com.cn/', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath('//tbody[@id="group_one"]//tr')
        fund_name = response.meta['ext']['fund_name']
        for row in rows:
            fund_date = row.xpath('.//td[2]//text()').extract_first()
            fund_nav = row.xpath('.//td[3]//text()').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y/%m/%d')
            item['nav'] = float(fund_nav)
            yield item
