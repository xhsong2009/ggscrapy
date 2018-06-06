# -*- coding: utf-8 -*-
import json
from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class TianTianFundSpider(GGFundNavSpider):
    name = 'FundNav_TianTianFund'
    sitename = '天天基金'
    channel = '天天基金'

    username = '13636340681'
    password = 'APTX4869'

    fps = [
        {
            'url': 'http://fund.eastmoney.com/gaoduan/FundTradeHighEnd.aspx?t=1&var=rankData&ss=all&jz=1&pt=all&nw=all&bm=all&is=all&sc=1y&st=desc&pi=1&pn=20&r=0.047422430673792704',
            'pg': 1,
        },
        {
            'url': 'http://fund.eastmoney.com/gaoduan/FundTradeHighEnd.aspx?t=1&var=rankData&ss=all&jz=3&pt=4&nw=all&bm=all&is=all&sc=1y&st=desc&pi=1&pn=20&r=0.17771536765939233',
            'pg': 1,
        }
    ]

    def start_requests(self):
        payload = {
            "loginParam": "MCUyQzAlMkMxMzYzNjM0MDY4MSUyQzFhMWE0NGI1YmU4ZDZlYzVjNjcwMTFjOTc2ZGM1ZDZkMTQ1Yzg2MGQ2MWI4ZWUyMzU4YmZlZmE0N2Q1ZTZhNTc0OGZkNDZkYWI1NWExZTk4MDkzNmE3YmUzMmM3NTYyNmZlYmM0YjIwOGQ1MmY2Yjc2MDdkMjgxYjEzNTUwNjdjYzZiZGI1MDZmZGQ2ZGI4NDliNjNmZTJmZTYxOGNjOWU4MzRjZWFhMWJmYTZjMzY1NzQ4YTY2NjA4MGVlMzAyNTlhMjg3MTgyYTBmOWMzMzQ2MjMxZGVlMzJiY2I0NmM2NDZkNWQyMGVjYTE1MDNjMmQyN2E2Nzc3ZDIwMjlhNmUlMkMlMkNodHRwJTNBJTJGJTJGZnVuZC5lYXN0bW9uZXkuY29tJTJGZ2FvZHVhbiUyRg=="}
        yield FormRequest(url='https://login.1234567.com.cn/LoginController.aspx/LoginNew',
                          body=json.dumps(payload),
                          method='POST'
                          )

    def parse_fund(self, response):
        datas = json.loads(response.text[13:-1])
        rows = datas['datas']
        for row in rows:
            fund_code = row['FUNDCODE']
            fund_name = row['FUNDNAME']
            self.ips.append({
                'url': 'http://fund.eastmoney.com/gaoduan/PinzhongF10DataApi.aspx?type=lsjz&fc={0}&pageindex=1&pagesize=10&lsjzSDate=&lsjzEDate=&r=0.94615975431393'.format(
                    fund_code),
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name, 'fund_code': fund_code}
            })

        tp = int(datas['allPages'])
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.fps.append({
                'url': 'http://fund.eastmoney.com/gaoduan/FundTradeHighEnd.aspx?t=1&var=rankData&ss=all&jz=1&pt=all&nw=all&bm=all&is=all&sc=1y&st=desc&pi={0}&pn=20&r=0.047422430673792704'.format(
                    pg),
                'ref': response.url,
                'pg': pg,
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        fund_code = ext['fund_code']
        datas = json.loads(response.text[11:])
        rows = datas['Datas']
        for row in rows:
            statistic_date = row['PDATE']
            nav = row['NAV']
            added_nav = row['ACCNAV']
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            if 'MUI' in row and 'SYI' in row:
                income_value_per_ten_thousand = row['MUI']
                d7_annualized_return = row['SYI']
            if income_value_per_ten_thousand and d7_annualized_return:
                item['d7_annualized_return'] = float(
                    d7_annualized_return) if d7_annualized_return is not None and d7_annualized_return != '' else None
                item['income_value_per_ten_thousand'] = float(
                    income_value_per_ten_thousand) if income_value_per_ten_thousand is not None and income_value_per_ten_thousand != '' else None
            else:
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        tp = int(datas['Pages'])
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://fund.eastmoney.com/gaoduan/PinzhongF10DataApi.aspx?type=lsjz&fc={0}&pageindex={1}&pagesize=10&lsjzSDate=&lsjzEDate=&r=0.94615975431393'.format(
                    fund_code, pg),
                'ref': response.url,
                'pg': pg,
                'ext': {'fund_name': fund_name, 'fund_code': fund_code},
            })
