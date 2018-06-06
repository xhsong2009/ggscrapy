# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-14

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy import FormRequest


class DiDaoFundSpider(GGFundNavSpider):
    name = 'FundNav_DiDaoFund'
    sitename = '深圳狄道投资'
    channel = '投资顾问'
    allowed_domains = ['www.didaofund.com']
    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.didaofund.com/product.php'}]

    def start_requests(self):
        yield FormRequest(url='http://www.didaofund.com/login.php',
                          formdata={'type': 'pc',
                                    'username': 'ZYYXSM',
                                    'pwd': 'ZYYXSM123'},
                          )

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="c3_b"]//@href').extract()
        fund_names = response.xpath('//div[@class="c3_b"]//@title').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.didaofund.com/', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="rightbar_cont_photo2"]/table[2]/tbody//tr')
        fund_name = response.meta['ext']['fund_name']
        for row in rows:
            fund_date = row.xpath('.//td[2]//text()').extract_first()
            fund_nav = row.xpath('.//td[3]//text()').extract_first()
            added_nav = row.xpath('.//td[4]//text()').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(fund_nav)
            item['added_nav'] = float(added_nav)
            yield item
