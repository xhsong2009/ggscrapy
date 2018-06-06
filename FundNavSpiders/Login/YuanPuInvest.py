# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YuanPuInvestSpider(GGFundNavSpider):
    name = 'FundNav_YuanPuInvest'
    sitename = '元普投资'
    channel = '投顾净值'

    username = '18625981663'
    password = 'benyi123456'

    def start_requests(self):
        yield FormRequest(url='http://www.yuanputouzi.com/index.php?m=member&c=index&a=public_login_ajax',
                          formdata={
                              'username': self.username,
                              'password': self.password
                          },
                          callback=self.start_pre_requests)

    def start_pre_requests(self, response):
        yield Request(url='http://www.yuanputouzi.com/products/zdgl/',
                      callback=self.parse_login_fund)

    def parse_login_fund(self, response):
        rows = response.xpath('//ul[@class="clearfix"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            self.fps.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_fund(self, response):
        rows = response.xpath('//ul[@class="fl pro-names"]/li')
        for row in rows:
            pro_id = row.xpath('./a/@href').re_first('([\d]+).html')
            self.ips.append({
                'url': 'http://www.yuanputouzi.com/index.php?m=content&c=index&a=ajax_page_list',
                'ref': response.url,
                'form': {
                    'proid': str(pro_id),
                    'page': '1'
                },
                'pg': 1
            })

    def parse_item(self, response):
        rows = response.xpath('//tr')[1:]
        for row in rows:
            fund_name = row.xpath('./td[1]/text()').extract_first()
            statistic_date = row.xpath('./td[3]/text()').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[4]/text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[5]/text()').re_first('[0-9.]+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        if len(rows) == 20:
            form = response.meta['form']
            pg = response.meta['pg'] + 1
            pro_id = form['proid']
            self.ips.append({
                'url': 'http://www.yuanputouzi.com/index.php?m=content&c=index&a=ajax_page_list',
                'ref': response.url,
                'form': {
                    'proid': str(pro_id),
                    'page': str(pg)
                },
                'pg': pg
            })
