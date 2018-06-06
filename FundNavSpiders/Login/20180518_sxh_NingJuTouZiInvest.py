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


class NingJuTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_NingJuTouZiInvest'
    sitename = '宁聚投资'
    channel = '投顾净值'
    allowed_domains = ['www.zjfunds.com']
    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [{'url': 'http://www.zjfunds.com/gsearch.aspx?curr_menu=products'}]

    def start_requests(self):
        yield Request(
            url='http://www.zjfunds.com/logon.aspx',
            callback=self.per_login)

    def per_login(self, response):
        __VIEWSTATE = \
        re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', response.text)[0]
        __VIEWSTATEGENERATOR = re.findall(r'__VIEWSTATEGENERATOR" value="(.*?)"', response.text)[0]
        __EVENTVALIDATION = re.findall(r'__EVENTVALIDATION" value="(.*?)"', response.text)[0]
        yield FormRequest(
            url='http://www.zjfunds.com/logon.aspx',
            formdata={
                '__VIEWSTATE': __VIEWSTATE,
                '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': __EVENTVALIDATION,
                'idcard': '13916427906',
                'password': 'ZYYXSM123',
                'btnSubmit': '立即登录',
                'chkAgree': 'on'
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='plist']//div[@class='ptb']")
        for row in rows:
            fund_name = row.xpath(".//td[@class='title']//text()").extract_first()
            nav = row.xpath(".//td[@class='prolist_r']/b//text()").extract_first()
            statistic_date = row.xpath(
                ".//td[@class='prolist_r']/p[@class='small-font']//text()").extract_first().replace('截至日期：', '')
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
