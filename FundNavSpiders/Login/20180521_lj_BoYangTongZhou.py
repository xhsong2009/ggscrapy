# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy import FormRequest


class BoYangTongZhouSpider(GGFundNavSpider):
    name = 'FundNav_BoYangTongZhou'
    sitename = '深圳伯洋同舟资产'
    channel = '投顾净值'
    allowed_domains = ['www.boyangtongzhou.com']
    phone = '13916427906'
    password = 'zyyxsm123'

    fps = [{'url': 'http://www.boyangtongzhou.com/list.php?id=16'}]

    def start_requests(self):
        yield FormRequest(url='http://www.boyangtongzhou.com/register.php?act=login',
                          formdata={'tel': '13916427906',
                                    'pwd': 'zyyxsm123'},
                          )

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="ht_special"]/div/ul//li//@href').extract()
        for url in href_list:
            ips_url = urljoin('http://www.boyangtongzhou.com/', url)
            self.ips.append({
                'url': ips_url,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//table[@class="table ke-zeroborder"]/tbody//tr')
        fund_name = response.xpath('//div[@class="content_msg"]/h1//text()').extract_first().replace('基金净值', '')
        for row in rows[1:]:
            fund_date = row.xpath('.//td[1]//text()').re_first('\d+-\d+-\d+')
            if fund_date is None:
                continue
            fund_nav = row.xpath('.//td[2]//text()').extract_first()
            added_nav = row.xpath('.//td[3]//text()').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date.replace(' ', ''), '%Y-%m-%d')
            item['nav'] = float(fund_nav)
            item['added_nav'] = float(added_nav)
            yield item
