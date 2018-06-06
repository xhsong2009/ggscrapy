# -*- coding: utf-8 -*-
import json
from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YiCunInvestSpider(GGFundNavSpider):
    name = 'FundNav_YiCunInvest'
    sitename = '一村投资'
    channel = '投资顾问'

    username = '17839170174'
    password = 'by123456'

    fps = [
        {
            'url': 'http://www.v-investment.com/api/pc/product/classify?by=INVEST_TARGET'
        }
    ]

    def start_requests(self):
        payload = {'userName': self.username, 'password': self.password, 'userType': '1'}
        yield FormRequest(url='http://www.v-investment.com/api/user/login',
                          body=json.dumps(payload),
                          method='POST',
                          headers={'Content-Type': 'application/json'})

    def parse_fund(self, response):
        collection = json.loads(response.text)['collection']
        for data in collection:
            rows = data['classifiedProducts']
            for row in rows:
                product_id = row['productId']
                fund_name = row['productShortName']
                self.ips.append({
                    'url': 'http://www.v-investment.com/api/pc/product/{0}/netValues?pageNum={1}'.format(product_id, 1),
                    'ref': response.url,
                    'pg': 1,
                    'ext': {'product_id': product_id, 'fund_name': fund_name}
                })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        product_id = ext['product_id']

        json_data = json.loads(response.text)
        rows = json_data['collection']
        if rows:
            for row in rows:
                statistic_date = row['netDate']
                nav = row['netValue']
                added_nav = row['accumulatedNet']

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

            pg = response.meta['pg'] + 1
            tp = int(json_data['property']['pages'])
            if pg <= tp:
                self.ips.append({
                    'url': 'http://www.v-investment.com/api/pc/product/{0}/netValues?pageNum={1}'.format(product_id, pg),
                    'ref': response.url,
                    'pg': pg,
                    'ext': {'product_id': product_id, 'fund_name': fund_name}
                })
