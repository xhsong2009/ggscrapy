# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy import FormRequest
import re


class QianHaiFangYuanInvestSpider(GGFundNavSpider):
    name = 'FundNav_QiMingLeTou'
    sitename = '启明乐投'
    channel = '投资顾问'
    allowed_domains = ['www.qmletou.com']
    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.qmletou.com/Products.aspx'}]

    def start_requests(self):
        yield FormRequest(url='http://www.qmletou.com/System/Users/AddUser.ashx',
                          formdata={'Command': 'Login',
                                    'UserName': '13916427906',
                                    'Password': 'ZYYXSM123'}
                          )

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="left_nav"]//@href').extract()
        fund_names = response.xpath('//div[@class="left_nav"]/ul/li//text()').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.qmletou.com/Products.aspx', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        date_info = re.findall('categories: \[(.*?)\]', response.text)[0]
        nav_info = re.findall('data: \[(.*?),\]', response.text)[1]
        added_nav_info = re.findall('data:\[(.*?),\]', response.text)[0]
        navs = nav_info.split(',')
        added_navs = added_nav_info.split(',')
        dates = date_info.split(',')
        for i in zip(dates, navs, added_navs):
            fund_date = i[0].replace("'", '')
            nav = i[1]
            added_nav = i[2]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item

