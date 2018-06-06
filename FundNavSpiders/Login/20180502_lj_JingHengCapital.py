# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-02

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy import FormRequest


class JingHengCapitalSpider(GGFundNavSpider):
    name = 'FundNav_JingHengCapital'
    sitename = '景恒资本'
    channel = '投顾净值'

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    fps = [{'url': 'http://www.jhcapital.com.cn/product.asp'}]

    def start_requests(self):
        yield FormRequest(url='http://www.jhcapital.com.cn/login_post.asp',
                          formdata={'LoginId': 'ZYYXSM',
                                    'Password': 'ZYYXSM123'
                                    },
                          )

    def parse_fund(self, response):
        fund_infos = response.xpath('//div[@class="container cclearfix"]/div/ul/li/ul//li')
        for url in fund_infos:
            fund_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first()
            ips_url = urljoin('http://www.jhcapital.com.cn/product.asp', fund_url)
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="product_conn"]/div[2]/table//tr')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            fund_date = row.xpath('.//td[2]//text()').extract_first()
            fund_nav = row.xpath('.//td[4]//text()').extract_first()
            added_nav = row.xpath('.//td[5]//text()').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y年%m月%d日')
            item['nav'] = float(fund_nav)
            item['added_nav'] = float(added_nav)
            yield item
