# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-02

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class HuiLiFundSpider(GGFundNavSpider):
    name = 'FundNav_HuiLiFund'
    sitename = '汇利资产'
    channel = '投顾净值'

    fps = [{'url': 'http://www.hlfund.com/detail.asp?id=55&bid=111&name=%BB%E3%C0%FB%BE%C5%C1%FA'}]

    def parse_fund(self, response):
        link_key = response.xpath('//td/a[contains(text(), "净值")]/@href').extract()
        fund_info = response.xpath('//td[@align="left" and @bgcolor="#F2F2F2"]/strong/text()').extract()

        for key, name in zip(link_key, fund_info):
            fund_link = urljoin('http://www.hlfund.com/', key)
            fund_name = name.replace(':', '')
            self.ips.append({
                'url': fund_link,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        nav_rows = response.xpath('//table[@width="96%"]//table/tbody/tr')
        for row in nav_rows[1:]:
            nav_info = row.xpath('td/font/text()').extract()
            fund_name = response.meta['ext']['fund_name']
            statistic_date = nav_info[0].replace(',', '').strip()
            nav = nav_info[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
            item['nav'] = float(nav) if nav is not None else None

            yield item
