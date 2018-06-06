# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class TianQiDeXingInvestSpider(GGFundNavSpider):
    name = 'FundNav_TianQiDeXingInvest'
    sitename = '天启德鑫'
    channel = '投顾净值'

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    fps = [{'url': 'http://www.year30.com/Cases'}]

    def start_requests(self):
        yield FormRequest(url='http://www.year30.com/userlogin?returnurl=',
                          formdata={
                              'Username': self.username,
                              'Password': self.password
                          })

    def parse_fund(self, response):
        href_list = response.xpath('//div[@id="view_list_21_1007"]//a[contains(text(),"净值")]/@href').extract()
        for href in href_list:
            self.ips.append({
                'url': 'http://www.year30.com' + href,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.css('tbody tr')[1:]
        for r in rows:
            td_dt = r.css('td:nth-child(1)::text').extract_first(default='')
            td_nav = r.css('td:nth-child(2)::text').extract_first(default='')
            td_add_nav = r.css('td:nth-child(3)::text').extract_first(default='')
            fund_name = response.css('h1.news_view_title::text').re_first('(.*)净值')
            if '分红' in td_nav or '分红' in td_add_nav:
                continue
            reg_number = re.compile('^[0-9]*.*[0-9]+$')
            nav = float(td_nav.strip()) if reg_number.match(str(td_nav)) else None
            if reg_number.match(str(td_add_nav)):
                if '+' in td_add_nav:
                    num1 = float(td_add_nav.split('+')[0].strip())
                    num2 = float(td_add_nav.split('+')[1].strip())
                    add_nav = num1 + num2
                else:
                    add_nav = float(td_add_nav.strip())
            else:
                add_nav = None

            if '20132-11-29' in td_dt:
                td_dt = '2013-11-29'
            date = td_dt.replace('-', '').strip()

            if nav or add_nav:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = nav
                item['added_nav'] = add_nav
                item['statistic_date'] = datetime.strptime(date, '%Y%m%d')

                yield item
