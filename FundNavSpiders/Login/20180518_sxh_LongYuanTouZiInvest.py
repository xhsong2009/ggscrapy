# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
from scrapy import Request
import re


class LongYuanTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_LongYuanTouZiInvest'
    sitename = '隆源投资'
    channel = '投资顾问'
    allowed_domains = ['www.longwininvestment.com']

    username = '13916427906'
    password = 'ZYYXSM123.'

    def start_requests(self):
        yield FormRequest(
            url='http://www.longwininvestment.com/Execution.aspx?type=login&t=user&tipurl=http://www.longwininvestment.com/default.aspx&tip_string=%E4%BC%9A%E5%91%98%E7%99%BB%E5%BD%95%E6%88%90%E5%8A%9F%EF%BC%81',
            formdata={'yonghuming': '13916427906',
                      'mima': 'ZYYXSM123.'},
            meta={'handle_httpstatus_list': [302]},
            callback=self.parse_home)

    def parse_home(self, response):
        yield Request(url='http://www.longwininvestment.com/page.aspx?id=1&classid=39', callback=self.parse_home_url)

    def parse_home_url(self, response):
        fund_urls = response.xpath("//div[@class='cp_list']//a")
        for url in fund_urls:
            fund_name = url.xpath('.//text()').extract_first().strip()
            fund_url = url.xpath('.//@href').extract_first()
            self.fps.append({
                'url': 'http://www.longwininvestment.com' + fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_fund(self, response):
        if 'iframe src=' in response.text:
            fund_url = re.findall(r'<iframe src="(.*?)" allowtransparency=', response.text)[0]
            fund_name = response.meta['ext']['fund_name']
            self.ips.append({
                'url': 'http://www.longwininvestment.com' + fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'url': fund_url},
                'pg': 1
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//tr")
        if len(rows) > 1:
            for row in rows[1:]:
                nav = row.xpath('./td[2]//text()').extract_first().replace('( ', '（').replace('(', '（')
                if '（' in nav:
                    nav = nav.split('（')[0]
                statistic_date = row.xpath('./td[1]//text()').extract_first().replace('年', '-').replace('月',
                                                                                                        '-').replace(
                    '日', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            pg = response.meta['pg']
            next_pg = int(pg) + 1
            url = response.meta['ext']['url']
            next_url = 'http://www.longwininvestment.com' + url + '&page=' + str(next_pg)
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name, 'url': url},
            })
