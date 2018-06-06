# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-04-27

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class HuiWeiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HuiWeiInvest'
    sitename = '汇蔚资产'
    channel = '投资顾问'

    fps = [{'url': 'http://www.huiweijijin.com/qxcp/hwcc/'}]

    def parse_fund(self, response):
        link_key = response.xpath('//ul[@class="sub_menu"]/li/a/@href').extract()
        for key in link_key:
            fund_link = urljoin('http://www.huiweijijin.com/', key.replace('../', ''))
            self.ips.append({
                'url': fund_link,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_info = response.xpath('//div[@class="sub"]/table/tbody/tr/td[2]/span/text()').extract()
        fund_name = fund_info[0]
        statistic_date = fund_info[4]
        nav = fund_info[1]
        added_nav = fund_info[2]

        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_name
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
        item['nav'] = float(nav) if nav is not None else None
        item['added_nav'] = float(added_nav) if added_nav is not None else None

        yield item
