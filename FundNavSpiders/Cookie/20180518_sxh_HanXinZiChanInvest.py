# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class HanXinZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_HanXinZiChanInvest'
    sitename = '瀚信资产'
    channel = '投顾净值'
    allowed_domains = ['www.hanxinchina.com']

    username = '朝阳永续'
    password = '88888888'
    cookies = 'UM_distinctid=1630499fe7e27d-0d959b16ddc151-3c604504-15f900-1630499fe7f40b; ASP.NET_SessionId=i2wz0mve4z1lxbuefagbjc45; CNZZDATA2812330=cnzz_eid%3D1535361529-1524790591-%26ntime%3D1526368672'
    fps = [
            {'url': 'http://www.hanxinchina.com/ProductInfo.aspx'},
        ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='r_product']/dl/dd//li//li")
        for url in fund_urls:
            fund_name = url.xpath('./a//text()').extract_first().strip()
            fund_url = url.xpath('./a/@href').extract_first()
            self.ips.append({
                'url': 'http://www.hanxinchina.com/cs.aspx?id='+fund_url.replace('ProductInfo.aspx?id=',''),
                'ref': response.url,
                'ext':{'fund_name':fund_name}
            })

    def parse_item(self, response):
        statistic_dates = re.findall(r'categories: \[(.*?)\]', response.text)[0].split(",")
        navs = re.findall(r'data: \[(.*?)\]', response.text)[0].split(",")
        added_navs = re.findall(r'data: \[(.*?)\]', response.text)[1].split(",")
        fund_name=response.meta['ext']['fund_name']
        if len(statistic_dates)>1:
            for row in zip(statistic_dates, navs, added_navs):
                statistic_date = row[0].replace("'", '')
                nav = row[1]
                added_nav = row[2]
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item


