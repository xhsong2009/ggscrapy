from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class YinTaiSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_YinTaiSecurities'
    sitename = '银泰证券'
    channel = '券商资管净值'

    fps = [
        {
            'url': 'https://biz.ytzq.com/web/bus/json',
            'form': {'funcNo': '101108'}
        }
    ]

    def parse_fund(self, response):
        funds = json.loads(response.text)['results']
        for fund in funds:
            fund_code = fund['fundcode']
            fund_name = fund['fundname']
            self.ips.append({
                'url': 'https://biz.ytzq.com/web/bus/json?funcNo=101109&pro_code={}&sortType=1'.format(fund_code),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = json.loads(response.text)['results']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = row['create_time']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')

            nav = row['relate_price']
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row['cumulative_net']
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item


