# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-10

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class CqJiHongSpider(GGFundNavSpider):
    name = 'FundNav_CqJiHong'
    sitename = '稷宏金融'
    channel = '投资顾问'
    allowed_domains = ['financ.cqjihong.com']
    start_urls = ['http://financ.cqjihong.com/Financ.aspx?pid=15']

    ips = [{'url': 'http://financ.cqjihong.com/Ajax/getprolist.ashx',
            'ref': 'http://financ.cqjihong.com/Financ.aspx?pid=15',
            'form': {
                'a': '0',
                'pid': '15',
                'T_ProductName': '稷宏1号证券私募基金'
            },
            'pg': 0
            }]

    def parse_item(self, response):

        if response.xpath('//tr[@class="old"]'):
            nav_rows = response.xpath('//tr[@class="old"]')
            for row in nav_rows:
                nav_info = row.xpath('td/text()').extract()
                statistic_date = nav_info[0]
                nav = nav_info[1]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = '稷宏1号证券私募基金'
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                yield item

            next_pg = response.meta['pg'] + 20
            self.ips.append({
                'url': 'http://financ.cqjihong.com/Ajax/getprolist.ashx',
                'ref': 'http://financ.cqjihong.com/Financ.aspx?pid=15',
                'form': {
                    'a': str(next_pg),
                    'pid': '15',
                    'T_ProductName': '稷宏1号证券私募基金'
                },
                'pg': next_pg
            })
