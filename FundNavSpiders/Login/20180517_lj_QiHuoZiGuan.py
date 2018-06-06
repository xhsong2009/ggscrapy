# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-17

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
from scrapy import Request, FormRequest


class QiHuoZiGuanSpider(GGFundNavSpider):
    name = 'FundNav_QiHuoZiGuan'
    sitename = '期货资管网'
    channel = '期货资管净值'

    def start_requests(self):
        yield Request(url='http://www.ziguan123.com/site/login?1=1', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        csrf_token = response.xpath('//meta[@name="csrf-token"]/@content').extract_first()
        yield FormRequest(url='http://www.ziguan123.com/site/login',
                          formdata={'_csrf': csrf_token, 'LoginForm[username]': '13916427906',
                                    'LoginForm[password]': 'ZYYXSM123', 'signup-button': '',
                                    'LoginForm[rememberMe]': '1'},
                          meta={'handle_httpstatus_list': [302],
                                'Content-Type': 'application/x-www-form-urlencoded'},
                          callback=self.parse_pre2_login)

    def parse_pre2_login(self, response):
        yield Request(url='http://www.ziguan123.com/product/ziguan', callback=self.parse_login)

    def parse_login(self, response):
        csrf_token = response.xpath('//meta[@name="csrf-token"]/@content').extract_first()
        self.fps.append(
            {'url': 'http://www.ziguan123.com/ajax/zgdatalist',
             'form': {'fundtype': '62', 'sort_name': 'Month1', 'sort_type': 'desc',
                      'page_index': '1', 'page_size': '100', 'companyid': ''},
             'headers': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'X-Requested-With': 'XMLHttpRequest',
                         'X-CSRF-Token': csrf_token,
                         'Referer': 'http://www.ziguan123.com/product/ziguan'}
             },
        )

    def parse_fund(self, response):
        funds = json.loads(response.text)['rawdata']['data']
        for fund in funds:
            fund_name = fund['productname']
            fund_id = fund['id']
            url = 'http://www.ziguan123.com/product/detail/{}'.format(fund_id)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name},
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//div[@class="w300 f14"]/table/tbody/tr')
        for row in rows:
            statistic_date = row.xpath('./td[1]').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[2]').re_first('>\s*([0-9.]+)\s*<')
            added_nav = row.xpath('./td[3]').re_first('>\s*([0-9.]+)\s*<')
            if statistic_date is None:
                continue
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)if nav is not None else None
            item['added_nav'] = float(added_nav)if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

