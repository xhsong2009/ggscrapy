# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
from scrapy import Request


class LaiYinYingXueTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_LaiYinYingXueTouZiInvest'
    sitename = '莱茵映雪投资'
    channel = '投资顾问'
    allowed_domains = ['www.lsl-invest.com']

    username = '18521028957'
    password = 'zyyx123456'

    fps = [{'url': 'http://www.lsl-invest.com/product/qjcp159/'}]

    def start_requests(self):
        yield FormRequest(url='http://www.lsl-invest.com//register.php?login=now',
                          formdata={'password': 'zyyx123456',
                                    'userphone': '18521028957',
                                    },
                          callback=self.parse_fund)

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='snow_fdiv']//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': fund_url + 'p1.html',
                'ref': response.url,
                'pg': 1
            })

    def parse_item(self, response):
        fund_name = response.xpath("//div[@class='sitemp clearfix']/h2//text()").extract_first().strip()
        rows = response.xpath("//div[@class='snow_value mt10']/div//tr")
        if rows:
            for row in rows:
                nav = row.xpath('./td[3]//text()').extract_first()
                statistic_date = row.xpath('./td[2]//text()').extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('/p' + str(pg) + '.html', '/p' + str(next_pg) + '.html')
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
            })
