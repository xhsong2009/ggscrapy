# -*- coding: utf-8 -*-
# Department：保障部
# Author：王卓诚
# Create_Date：2018-05-28

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class JinShiTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_JinShiTouZiInvest'
    sitename = '金石投资'
    channel = '投资顾问'
    allowed_domains = ['www.gsfund.cn']

    username = '点点'
    password = '123456'
    cookies = 'PHPSESSID=e1suj9gubpi6e2kfgraf56g474'

    fps = [{'url': 'http://www.gsfund.cn/Products/index.html'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//li[@class='pw-list-small pw-list-small-on'][3]//@href").extract()
        fund_names = response.xpath("//a[@id='zhanxian']//text()").extract()
        for url in zip(fund_urls, fund_names):
            fund_url = url[0]
            fund_name = url[1]
            self.ips.append({
                'url': 'http://www.gsfund.cn' + fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='pw-right-content']//tr")
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            date = row.xpath("./td[2]//text()").extract()
            statistic_date = ''.join(date)
            nav = row.xpath("./td[3]//text()").extract_first()
            if statistic_date:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
