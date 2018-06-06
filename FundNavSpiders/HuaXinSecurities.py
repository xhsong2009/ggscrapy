# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-07

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class HuaXinSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_HuaXinSecurities'
    sitename = '华信证券'
    channel = '券商资管净值'

    # username = '13916427906'
    # password = 'ZYYXSM123'
    fps = [{
        'url': 'https://trade.shhxzq.com/api/product/queryFinanceSuperMarket',
        'headers': {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'deviceId': 'Bva7x0Ha9HTon9RiJLhtSk',
            'browserName': 'Chrome',
            'channel': 'P',
            'Referer': 'https://trade.shhxzq.com/financialMarket?productType=3', },
        'form': {
            'pageSize': '500',
            'pageNo': '1',
            'productType': '3',
        },
    }]

    def parse_fund(self, response):
        funds_list = json.loads(response.text)['resultData']['result']
        for fund in funds_list:
            code = fund['productid'][-6:]
            # 七日年化收益率;单位净值,年化业绩比较基准
            f_type = fund['yieldType']
            self.ips.append({
                'url': 'http://www.shhxzq.com/web/zcgl/jhjzList.jsp?FundCode=' + code + '&pageIndex=1&pageSize=9999',
                'ref': response.url,
                'ext': f_type
            })

    def parse_item(self, response):
        fund_type = response.meta['ext']
        funds_list = json.loads(response.text)['result']
        for i in funds_list:
            statistic_date = i['pubtime']
            fund_name = i['name']

            item = GGFundNavItem()
            if '七日年化收益率' in fund_type:
                ten_thousand = i['dwjz']
                d7_annualized = i['ljjz']
                item['income_value_per_ten_thousand'] = float(ten_thousand) if ten_thousand != '' else None
                item['d7_annualized_return'] = float(d7_annualized) if d7_annualized != '' else None
            else:
                nav = i['dwjz']
                added_nav = i['ljjz']
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            yield item
