from datetime import datetime, date
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class TianShengQiaoSpider(GGFundNavSpider):
    name = 'FundNav_TianShengQiao'
    sitename = '天生桥'
    channel = '投资顾问'
    ips = []
    for id in ['1', '4']:
        ips.append({
            'url': 'https://naturebridge-asset.com/api/public/funds/' + id + '/netvalues/start/2001-01-01/end/' + date.isoformat(datetime.now()),
            'headers': {'authorization': 'Basic Z29nb2FsOmMzbVJjMFg4'}
        })

    def parse_item(self, response):
        fund_name = json.loads(response.text)['name']
        rows = json.loads(response.text)['net_values']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = row['date']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row['value']
            item['nav'] = float(nav) if nav is not None else None

            yield item

