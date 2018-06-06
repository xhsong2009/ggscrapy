# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-11

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LiYingCapitalSpider(GGFundNavSpider):
    name = 'FundNav_LiYingCapital'
    sitename = '深圳力盈资本'
    channel = '投资顾问'
    allowed_domains = ['www.szlyzb.com']
    start_urls = ['http://www.szlyzb.com/index.php/lycp']

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'PHPSESSID=u0s1cs2cn2oupc1i75dftti1r2'

    ips = [{'url': 'http://www.szlyzb.com/index.php/lycp',
            'ref': 'http://www.szlyzb.com/'}]

    def parse_item(self, response):
        fund_info = response.xpath('//div[@style="height: 400px !important; overflow-x: hidden;"]//tr')

        for row in fund_info:
            nav_info = row.xpath('td/text()').extract()
            fund_name = nav_info[0].strip()
            statistic_date = nav_info[1].strip()
            nav = nav_info[2].strip()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None
            yield item
