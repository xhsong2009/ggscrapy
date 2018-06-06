# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_Date : 2018-05-18
# Alter_Date : 2018-05-24

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import calendar


class HaiZhengTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HaiZhengTouZiInvest'
    sitename = '海证投资'
    channel = '投资顾问'
    allowed_domains = ['www.zgqhtzw.com']
    username = '13916427906'
    password = 'ZYYX888'

    cookies = 'safedog-flow-item=; kerenLogin=userid=13916427906; popped=yes; productpopped=yes'
    fps = [
            {'url': 'http://www.zgqhtzw.com/fund.aspx?sClass=1&sType=3'},
        ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@id='mainInLeft']/ul//li")
        for url in fund_urls:
            fund_name = url.xpath('./a/@title').extract_first().strip()
            fund_url = url.xpath('./a/@href').extract_first()
            self.ips.append({
                'url': 'http://www.zgqhtzw.com/'+fund_url,
                'ref': response.url,
                'ext':{'fund_name':fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name'].replace('（已终结）', '')
        nav = response.xpath("//div[@class='text_jz']/table[@class='d_t']/tbody/tr[2]/td[2]//text()").extract_first()
        added_nav = response.xpath("//div[@class='text_jz']/table[@class='d_t']/tbody/tr[2]/td[2]//text()").extract_first()
        date = response.xpath("//div[@class='text_jz']/table[@class='d_t']/tbody/tr[4]/td[2]//text()").extract_first()
        if len(date) < 10:
            date_info = date.replace('年', '-').replace('月', '')
            year = date_info[0:4]
            if date_info[-2] == '1':
                month = '1' + date_info[-1]
            else:
                month = date_info[-1]
            wday, monthrange = calendar.monthrange(int(year), int(month))
            weekday = calendar.weekday(int(year), int(month), monthrange)
            if weekday == 5:
                monthrange = monthrange - 1
            elif weekday == 6:
                monthrange = monthrange - 2
            statistic_date = date_info + '-' + str(monthrange)
        else:
            statistic_date=date
        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_name
        item['nav'] = float(nav) if nav is not None else None
        item['added_nav'] = float(added_nav) if nav is not None else None
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
        yield item


