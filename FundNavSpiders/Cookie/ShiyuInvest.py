from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request, FormRequest
import json


class ShiYuFundSpider(GGFundNavSpider):
    name = 'FundNav_ShiYuFund'
    sitename = '世域投资'
    channel = '投资顾问'

    username = '13916427906'
    verifycode = '167528'
    Authorization = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjI6NzoxMzkxNjQyNzkwNiIsIm9yaWdfaWF0IjoxNTI3MTIzMzU4LCJ1c2VyX2lkIjozMDEsImVtYWlsIjoiIiwiZXhwIjoxNTMyMzA3MzU4fQ.tpBa-6-NIWbiIJVrdUnkU3Gp00vO4HtOW75mC1Ssvhk'

    def start_requests(self):
        yield FormRequest(
            url='http://www.jdoor.cn/api/customerlogin/',
            method='POST',
            body=json.dumps({"phone": "13916427906", "verifycode": self.verifycode}),
            headers={
                'org': '1819b573-3e70-4adc-95f1-d8a2b8a09787',
                'Content-Type': 'application/json',
                'Pragma': 'no-cache',
                'Accept': '*/*'},
            callback=self.parse_login)

    def parse_login(self, response):
        yield Request(
            url='http://www.jdoor.cn/api/products/',
            method='GET',
            headers={
                'Authorization': self.Authorization,
                'org': '1819b573-3e70-4adc-95f1-d8a2b8a09787',
                'Content-Type': 'application/json',
                'Accept': '*/*',
            },
            callback=self.parse_fund)

    def parse_fund(self, response):
        funds = json.loads(response.text)['results']
        for fund in funds:
            self.ips.append({
                'url': 'http://www.jdoor.cn/api/products/' + str(
                    fund['id']) + '/comparenetvalue/all/',
                'method': 'GET',
                'headers': {
                    'Authorization': self.Authorization,
                    'org': '1819b573-3e70-4adc-95f1-d8a2b8a09787',
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                },
                'ext': {'fund_name': fund['short_name']}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        datas = json.loads(response.text)['netvalues']
        for data in datas:
            fund_date = data['value_date']
            nav = data['unit_value']
            added_nav = data['total_value']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item
