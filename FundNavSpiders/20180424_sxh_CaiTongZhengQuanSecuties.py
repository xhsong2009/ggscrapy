# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# Department：保障部
# Author：宋孝虎
# Create_Date：2018-04-24

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class CaiTongZhengQuanSecutiesSpider(GGFundNavSpider):
    name = 'FundNav_CaiTongZhengQuanSecuties'
    sitename = '财通证券'
    channel = '券商资管净值'
    allowed_domains = ['www.ctzg.com']

    fps = [
        {
            'url': 'http://www.ctzg.com/servlet/json?funcNo=904504&page=1&numPerPage=500&conditionArr=%25E5%2585%25A8%25E9%2583%25A8%252C%25E5%2585%25A8%25E9%2583%25A8%252C%25E5%2585%25A8%25E9%2583%25A8%252C%25E5%2585%25A8%25E9%2583%25A8%252C%25E5%2585%25A8%25E9%2583%25A8&jjjc=&sort=%25E5%258F%2591%25E5%25B8%2583%25E6%2597%25B6%25E9%2597%25B41',
            'pg': 1}
    ]

    def parse_fund(self, response):
        funds = json.loads(response.text)['results'][0]['data']
        for fund in funds:
            type = fund['name']
            fund_code = fund['jjdm']
            self.ips.append({
                'url': 'http://www.ctzg.com/servlet/json?funcNo=904505&code=' + fund_code + '&catalogIds=&page=1&numPerPage=500',
                'ref': response.url,
                'pg': 1,
                'ext': {'type': type}
            })
        pg = response.meta['pg']
        next_pg = pg + 1
        self.fps.append({
            'url': response.url.replace('&page=' + str(pg), '&page=' + str(next_pg)),
            'ref': response.url,
            'pg': next_pg
        })

    def parse_item(self, response):
        type = response.meta['ext']['type']
        nav_info = json.loads(response.text)
        rows = nav_info['results'][0]['data']
        for row in rows:
            fund_name = row['fundnameeng']
            nav = row['tab_rate_1']
            added_nav = row['tab_rate_2']
            d7_annualized_return = row['tab_rate_2']
            income_value_per_ten_thousand = row['tab_rate_1']
            statistic_date = row['tradedate']
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            if type == '七日年化收益率':
                item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand)if income_value_per_ten_thousand else None
                item['d7_annualized_return'] = float(d7_annualized_return)if d7_annualized_return else None
            else:
                item['nav'] = float(nav) if nav is not None and nav != '' else None
                item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        if len(rows) > 1:
            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('&page=' + str(pg), '&page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'type': type}
            })
