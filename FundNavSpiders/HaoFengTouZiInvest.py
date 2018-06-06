# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-04-26

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest


class HaoFengTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HaoFengTouZiInvest'
    sitename = '昊沣投资'
    channel = '投顾净值'

    fps = [{'url': 'http://www.goodwind.me/index.php'}]

    def start_requests(self):
        yield FormRequest(url='http://www.goodwind.me/disclaimer.php?ret=%3F',
                          formdata={'ret': '?'},
                          callback=self.parse_fund)

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='f_l newbg']/table[@class='table pr_view']//tr//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.goodwind.me/' + fund_url,
                'ref': response.url,
            })

    def parse_item(self, response):
        rows = response.xpath("//tr")
        for row in rows[1:]:
            fund_name = row.xpath("./td[1]//text()").extract_first()
            statistic_date = row.xpath("./td[2]//text()").extract_first()
            nav = row.xpath("./td[3]//text()").extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
