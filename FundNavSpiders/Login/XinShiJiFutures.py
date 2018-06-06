# -*- coding: utf-8 -*-

from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem
from scrapy import FormRequest
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from datetime import datetime


class XinShiJiFuturesSpider(GGFundNavSpider):
    name = 'FundNav_XinShiJiFutures'
    sitename = '新世纪期货'
    channel = '发行机构'

    username = '18638357950'
    password = '123456'
    password_md5 = 'e10adc3949ba59abbe56e057f20f883e'

    fps = [
        {
            'url': 'http://www.zjncf.com.cn/asset-management/product-value',
            'pg': 0
        }
    ]

    def start_requests(self):
        yield FormRequest(url='http://www.zjncf.com.cn/user/login',
                          formdata={
                              'accountName': self.username,
                              'password': self.password_md5,
                          })

    def parse_fund(self, response):
        rows = response.xpath('//ul[@class="product-value-list"]/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })
        count = int(response.xpath('//div[@id="Pagination"]/@data-pagecount').extract_first())
        tp = int(count / 20 if count % 20 == 0 else count // 20 + 1)
        pg = response.meta['pg'] + 1
        if pg < tp:
            self.fps.append({
                'url': 'http://www.zjncf.com.cn/asset-management/product-value?pageNum={0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })

    def parse_item(self, response):
        row = response.xpath('//div[@class="news-content"]/div/div').xpath('string(.)')
        fund_name = row.re_first(r'([^/]+)截[止|至]').strip()
        statistic_date = row.re_first(r'(\d+年\d+月\d+日)')
        nav = row.re_first(r'计划份额净值：([0-9.]+)')
        added_nav = row.re_first(r'累积净值([0-9.]+)')

        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_name
        item['nav'] = float(nav)
        item['added_nav'] = float(added_nav) if added_nav is not None else added_nav
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
        yield item
