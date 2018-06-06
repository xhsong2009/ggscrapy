# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-09

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class ShiPuInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShiPuInvest'
    sitename = '深圳石浦投资'
    channel = '投资顾问'
    allowed_domains = ['www.sptz.com']
    start_urls = ['http://www.sptz.com/products.html']

    ips = [{'url': 'http://www.sptz.com/products.html'}]

    def parse_item(self, response):
        fund_name = response.xpath(
            '//table[@class="product_table ke-zeroborder"]//tr[1]/td[2]/text()').extract_first().strip()
        nav_rows = response.xpath('//div[@class="shop_div"]/table[@class="ke-zeroborder"]//tr')

        for nav_row in nav_rows[1:]:
            nav_td = nav_row.xpath('td//text()').extract()
            if nav_td:
                if nav_td[1].strip() != '日期':
                    if nav_td[1].strip() == '2017/12/01':
                        statistic_date = nav_td[1].strip()
                        nav = 1.0544
                    else:
                        statistic_date = nav_td[1].strip()
                        nav = nav_td[2].strip()

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                    item['nav'] = float(nav) if nav else None

                    yield item
