# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-08
# Alter_date : 2018-05-22

from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class PingAnZhengQuanSecuritySpider(GGFundNavSpider):
    name = 'FundNav_PingAnZhengQuanSecurity'
    sitename = '平安证券'
    channel = '券商资管净值'
    allowed_domains = ['stock.pingan.com']

    def start_requests(self):
        payload = {"body": {}, "requestId": "c1f177fa16c13202f9934b71db7fc986"}
        yield Request(url='https://stock.pingan.com/restapi/contentservice/openWeb/collectFinancialList',
                      body=json.dumps(payload),
                      method='POST',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                          'Referer': 'https://stock.pingan.com/static/webinfo/assetmanage/index.html',
                          'Content-Type': 'application/json',
                      },
                      callback=self.parse_fund)

    def parse_fund(self, response):
        fund_infos = json.loads(response.text)
        fund_ids = fund_infos['results']['productList']
        for id in fund_ids:
            fund_name = id['fundName'].strip()
            fund_id = id['id']
            self.ips.append({
                'url': "https://stock.pingan.com/restapi/contentservice/openWeb/queryCFProductHistory",
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'fund_id': fund_id, 'isnav': '1'},
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'Content-Type': 'application/json;charset=UTF-8',
                },
                'body': json.dumps(
                    {"body": {"pageSize": 15, "pageNo": 1, "id": fund_id, "proType": 0, "startDate": "",
                              "endDate": "", "pageType": 0}, "requestId": "b9024b74c270802d7086907c911d8aff"}),
                'pg': 1
            })
        fund_idss = fund_infos['results']['cashList']
        for ids in fund_idss:
            fund_name = ids['fundName'].strip()
            fund_id = ids['id']
            self.ips.append({
                'url': "https://stock.pingan.com/restapi/contentservice/openWeb/queryCFProductHistory",
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'fund_id': fund_id, 'isnav': '0'},
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'Content-Type': 'application/json;charset=UTF-8',
                },
                'body': json.dumps(
                    {"body": {"pageSize": 15, "pageNo": 1, "id": fund_id, "proType": 1, "startDate": "",
                              "endDate": "", "pageType": 0}, "requestId": "202ecace8fe64d995d2f271912f7d7ee"}), })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        is_nav = response.meta['ext']['isnav']
        nav_info = json.loads(response.text)
        rows = nav_info['results']['dataList']
        for row in rows:
            statistic_date = row['tradeDate']
            item = GGFundNavItem()
            if is_nav == '1':
                nav = row['nav']
                added_nav = row['accumulativeNav']
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
            else:
                income_value_per_ten_thousand = row['fundIncome']
                d7_annualized_return = row['yield']
                annualized_return = row['fundDayIncome']
                item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand)
                item['d7_annualized_return'] = float(d7_annualized_return)
                item['annualized_return'] = float(annualized_return)
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name.replace(' ', '')

            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
