# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhiXinInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZhiXinInvest'
    sitename = '无锡智信投资'
    channel = '投资顾问'

    username = '123'
    password = '123456'
    fps = [{'url': 'http://www.zxwealth.com.cn/zqjy',
            'ext': {'type': 'start_url'}}]

    def start_requests(self):
        yield FormRequest(url='http://www.zxwealth.com.cn/login?loggedout=true',
                          formdata={
                              'log': self.username,
                              'pwd': self.password,
                              'rememberme': 'forever',
                              'wp-submit': '登录',
                              'redirect_to': 'http://www.zxwealth.com.cn/wp-admin/',
                              'testcookie': '1'
                          })

    def parse_fund(self, response):
        response_type = response.meta['ext']['type']
        if response_type == 'start_url':
            fps_url_list = response.css('div.left_mian a::attr(href)').extract()
            name_list = response.css('div.left_mian a::text').extract()
            for fps_url, fname in zip(fps_url_list, name_list):
                self.fps.append({
                    'url': fps_url,
                    'ref': response.url,
                    'ext': {'type': 'fps'}
                })

        if response_type == 'fps':
            ips_url = response.xpath(
                '//div[@class="tab fb f14 white"]//a[contains(text(),"历史业绩")]/@href').extract_first()
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'type': 'ips'}
            })

    def parse_item(self, response):
        rows = response.css('tbody#result tr')
        fund_name = response.css('div.right_mian h2::text').re_first('\S+')
        for r in rows:
            td_dt = r.css('td:nth-child(2)::text').extract_first(default='')
            td_nav = r.css('td:nth-child(3)::text').extract_first(default='')
            td_add_nav = r.css('td:nth-child(4)::text').extract_first(default='')

            if '2017-03-34' in td_dt:
                td_dt = '2017-03-24'

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(td_nav.strip()) if td_nav.strip() else None
            item['added_nav'] = float(td_add_nav.strip()) if td_add_nav.strip() else None
            item['statistic_date'] = datetime.strptime(td_dt.strip(), '%Y-%m-%d') if td_dt.strip() else None

            yield item
