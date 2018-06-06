# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YunChengTaiInvestSpider(GGFundNavSpider):
    name = 'FundNav_YunChengTaiInvest'
    sitename = '云程泰投资'
    channel = '投顾净值'

    username = '本易123456'
    password = 'by123456'

    def start_requests(self):
        yield Request(url='http://www.yctchina.com.cn/index.html', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.yctchina.com.cn/member/index_do.php',
                          formdata={
                              'userid': self.username,
                              'pwd': self.password,
                              'fmdo': 'login',
                              'dopost': 'login',
                              'gourl': ''
                          },
                          headers={
                              'Content-Type': 'application/x-www-form-urlencoded'
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps = [{
            'url': 'http://www.yctchina.com.cn/a/yincang/index.html',
            'ref': response.url
        }]
        yield self.request_next()

    def parse_fund(self, response):
        funds = response.xpath('//table[@id="cp_table"]/tr/td[last()]/a/@href').extract()
        for url in funds:
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        datas = response.xpath('//*[@id="pd_table"]//tr')
        next_url = response.xpath('/html/body/div[4]//ul[@class="pagelist"]/li/a[text()="下一页"]/@href').extract_first()
        for row in datas[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = row.xpath('./td[1]/text()').extract_first()
            item['channel'] = self.channel
            item['url'] = response.url
            nav = row.xpath('./td[2]/text()').extract_first()
            item['nav'] = float(nav)
            statistic_date = row.xpath('./td[5]/text()').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
        if next_url is not None and next_url != 'javascript:void(0);':
            url = urljoin(get_base_url(response), next_url)
            self.ips.append({'url': url, 'ref': response.url})

