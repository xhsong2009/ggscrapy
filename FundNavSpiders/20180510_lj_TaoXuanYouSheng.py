# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-09

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
import re
import time
from scrapy import FormRequest


class TaoXuanYouShengSpider(GGFundNavSpider):
    name = 'FundNav_TaoXuanYouSheng'
    sitename = '前海韬选优胜资产'
    channel = '投顾净值'
    allowed_domains = ['www.txysa.com']

    username = '13916427906'
    password = 'ZYYXSM123'
    fps = [{'url': 'http://www.txysa.com/product.php'}]

    def start_requests(self):
        yield FormRequest(url='http://www.txysa.com/login_do.php',
                          formdata={'username': '13916427906',
                                    'pwd': 'ZYYXSM123',
                                    'authcode': '',
                                    'action': 'login'},
                          callback=self.parse_fund)

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="zycont w1100 clearfix"]/div/div[2]/ul//li//@href').extract()
        fund_names = response.xpath('//div[@class="zycont w1100 clearfix"]/div/div[2]/ul//li//@title').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.txysa.com/', url.replace('product.', 'chartdata.').replace('php?c', 'php?'))
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        funds_info = re.findall(r"var jz_date=(.*?)];var hs_date", response.text)[0]
        fund_info = re.findall(r"\[(\d+),(\d{1,2}.\d+)\]", funds_info)
        fund_name = response.meta['ext']['fund_name']
        for i in fund_info:
            fund_date = time.strftime("%Y-%m-%d", time.localtime(int(i[0]) / 1000))
            fund_nav = i[1]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(fund_nav) if fund_nav is not None else None
            yield item
