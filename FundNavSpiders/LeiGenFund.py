from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
from datetime import date, datetime


class LeiGenFundSpider(GGFundNavSpider):
    name = 'FundNav_LeiGenFund'
    sitename = '上海雷根资产'
    channel = '投顾净值'

    fps = [
        {
            'url': 'http://m.reganfund.com/weChat/fundQueryNew',
            'body': "{'fundInfo': '', 'top100': '1', 'tagIds': ''}",
            'headers': {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/json; charset=UTF-8'
            }
        }
    ]

    def parse_fund(self, response):
        funds = json.loads(response.text)['resultList']
        for fund in funds:
            if fund['fundName'] == '雷根9号基金':
                fund_code = 'S33704'
            else:
                fund_code = fund['fundCode']
            body = json.dumps(
                {"fundCode": fund_code, "startDate": "2001-01-01", "endDate": date.isoformat(datetime.now())})
            self.ips.append({
                'url': 'http://m.reganfund.com/weChat/dataOverview',
                'body': body,
                'headers': {'Content-Type': 'application/json; charset=UTF-8'}

            })

    def parse_item(self, response):
        rows = json.loads(response.text)['result']['value']
        fund_name = json.loads(response.text)['fundName']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = 'http://www.reganfund.com/product.html'
            item['fund_name'] = fund_name

            statistic_date = row['tradingDate']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row['nav']
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row['nav']
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item

