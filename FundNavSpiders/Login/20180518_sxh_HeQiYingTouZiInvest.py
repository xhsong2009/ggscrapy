# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest


class HeQiYingTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HeQiYingTouZiInvest'
    sitename = '上海鹤骑鹰投资'
    channel = '投资顾问'
    allowed_domains = ['www.heqiying.com']

    username = '15090191207'
    password = '123456x'

    fps = [
        {'url': 'http://www.heqiying.com/fund_mng/desktop/networths'},
        {'url': 'http://www.heqiying.com/fund_mng/desktop/networthsclosed'},
    ]

    def start_requests(self):
        yield FormRequest(
            url='http://www.heqiying.com/fund_mng/resources/j_spring_security_check',
            formdata={
                'username': '15090191207',
                'password': '123456x',
            })

    def parse_fund(self, response):
        fund_urls = response.xpath("//@data-href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.heqiying.com' + fund_url,
                'ref': response.url,
            })

    def parse_item(self, response):
        fund_name = response.xpath("//div[@class='col-md-9']/h4//text()").extract_first()
        rows = response.xpath("//div[@id='value']//div")
        for row in rows:
            statistic_date = row.xpath("./div[@class='col-lg-4'][1]//text()").extract_first()
            nav = row.xpath("./div[@class='col-lg-4'][2]//text()").extract_first()
            added_nav = row.xpath("./div[@class='col-lg-4'][3]//text()").extract_first()
            if statistic_date:
                statistic_date = statistic_date.strip()
                nav = nav.strip()
                added_nav = added_nav.strip()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
