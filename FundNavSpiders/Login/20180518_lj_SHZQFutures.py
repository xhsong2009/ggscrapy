# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-18
# Alter_date : 2018-05-23

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
import re


class SHZQFuturesSpider(GGFundNavSpider):
    name = 'FundNav_SHZQFutures'
    sitename = '上海中期期货'
    channel = '期货净值'
    allowed_domains = ['www.shcifco.com']
    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    fps = [{
               'url': 'http://www.shcifco.com/plus/list.php?tid=168&TotalResult=25&nativeplace=0&infotype=0&keyword=&fxlx=&cplx=&cpjs=&tzcl=&PageNo=1'}, ]

    def start_requests(self):
        yield FormRequest(url='http://www.shcifco.com/relo/shangxian_ac.php',
                          formdata={'username': 'ZYYXSM',
                                    'password': 'ZYYXSM123',
                                    'submit': '', })

    def parse_fund(self, response):
        fund_hrefs = response.xpath("//div[@class='cfzx_main3_main']/div[4]//ul//li[2]//@href").extract()
        fund_names = response.xpath("//div[@class='cfzx_main3_main']/div[4]//ul//li[2]//a//text()").extract()
        for (fund_href, name) in zip(fund_hrefs, fund_names):
            urls = re.findall('.*/(.*?).html', fund_href)[0]
            fund_url = 'http://www.shcifco.com/plus/show_jz.php?wdid=' + urls
            fund_name = name.strip()
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}})

        pg = response.url.replace(
            'http://www.shcifco.com/plus/list.php?tid=168&TotalResult=25&nativeplace=0&infotype=0&keyword=&fxlx=&cplx=&cpjs=&tzcl=&PageNo=',
            '')
        next_pg = int(pg) + 1

        if next_pg <= 2:
            self.fps.append({
                'url': 'http://www.shcifco.com/plus/list.php?tid=168&TotalResult=25&nativeplace=0&infotype=0&keyword=&fxlx=&cplx=&cpjs=&tzcl=&PageNo=' + str(
                    next_pg),
                'ref': response.url})

    def parse_item(self, response):
        rows = response.xpath('//div[@class="cfzx_tjtg"]/div[2]//ul')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[2:]:
            statistic_date = row.xpath('.//li[1]//text()').extract_first()
            navs = row.xpath('.//li[2]//text()').extract_first()
            added_navs = row.xpath('.//li[3]//text()').extract_first()
            if (statistic_date is not None and navs is not None and added_navs is not None) and ('/' not in navs) and (
                    '.' not in statistic_date):
                date = statistic_date.strip()
                nav = navs.strip()
                added_nav = added_navs.strip()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav) if '-' not in added_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y/%m/%d')
                yield item

