# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-04

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class YongYuanFundSpider(GGFundNavSpider):
    name = 'FundNav_YongYuanFund'
    sitename = '嘉兴永源投资'
    channel = '投资顾问'

    fps = [{'url': 'http://www.yongyuanfund.com/Index.aspx'}]

    def parse_fund(self, response):
        funds = response.xpath('//div[@class="netWorth"]/table/tr')[1:]
        for fund in funds:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund.xpath('./td[1]/a/text()').extract_first()
            statistic_date = fund.xpath('./td[5]/text()').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = fund.xpath('./td[2]/text()').extract_first()
            item['nav'] = float(nav) if nav is not None else None
            yield item

            url = fund.xpath('./td[1]/a/@href').extract_first()
            url = urljoin('http://www.yongyuanfund.com/', url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        nav_rows = response.xpath('//div[@class="content"]/table//tr')
        for row in nav_rows[1:]:
            nav_info = row.xpath('td/text()').extract()
            fund_name = nav_info[0]
            statistic_date = nav_info[4]
            nav = nav_info[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None

            yield item
