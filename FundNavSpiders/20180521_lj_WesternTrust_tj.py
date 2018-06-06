# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
import re


class WesternTrustSpider(GGFundNavSpider):
    name = 'FundNav_WesternTrust'
    sitename = '西部信托'
    channel = '信托净值'
    allowed_domains = ['www.wti-xa.com']
    fps = [{'url': 'http://www.wti-xa.com/gongsixinwen_single_jingzhi.jsp?pageIndex=1&pageSize=10&pageFlag=3'}]

    def parse_fund(self, response):
        names_list = response.xpath('//div[@class="content"]/div[2]//tr//@title').extract()
        href_list = response.xpath('//div[@class="content"]/div[2]//tr//@href').extract()
        for name, fund_href in zip(names_list, href_list):
            if ('特定产品' not in name) and ('jm_login.jsp' not in fund_href):
                fund_name = name
                href = fund_href
                ips_url = (urljoin('http://www.wti-xa.com/', href))
                self.ips.append({
                    'url': ips_url,
                    'ref': response.url,
                    'pg': 1,
                    'ext': {'fund_name': fund_name},
                })
        end_page = re.findall('<DIV class=pageinfo>共 (.*?)页，跳转到', response.text)[0]
        pg = response.url.replace('http://www.wti-xa.com/gongsixinwen_single_jingzhi.jsp?pageIndex=', '').replace(
            '&pageSize=10&pageFlag=3', '')
        next_pg = int(pg) + 1

        if next_pg <= int(end_page):
            self.fps.append({
                'url': 'http://www.wti-xa.com/gongsixinwen_single_jingzhi.jsp?pageIndex=' + str(
                    next_pg) + '&pageSize=10&pageFlag=3',
                'ref': response.url,
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//div[@class="box"]/div/div//tr')
        for row in rows[1:]:
            statistic_date = row.xpath('.//td[1]//text()').extract_first()
            if '分红' not in statistic_date:
                nav = row.xpath('.//td[2]//text()').extract_first()
                added_nav = row.xpath('.//td[3]//text()').extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if ('-' not in nav) else None
                item['added_nav'] = float(added_nav) if ('-' not in added_nav) else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
