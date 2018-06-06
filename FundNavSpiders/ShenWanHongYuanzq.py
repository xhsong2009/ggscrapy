# -*- coding: utf-8 -*-
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
import re


class ShenHongWanYuanzqSpider(GGFundNavSpider):
    name = 'FundNav_ShenWanHongYuanzq'
    sitename = '申万宏源证券(原申万)'
    channel = '券商资管净值'

    fps = [
        {
            'url': 'http://www.sywg.com/sywg/busiProduct.do?method=getProductProList&page=1',
            'pg': 1
        }
    ]

    def parse_fund(self, response):
        funds = json.loads(response.text.replace("'", "\""))['pros']
        for fund in funds:
            fund_name = fund['fundName']
            fund_code = fund['productCode']
            type = fund['showType']
            self.ips.append({
                'url': 'http://www.sywg.com/sywg/busiProduct.do?method=getProductNetValueList&productCode='+ fund_code
                       + '&showSize=10&pageNo=1&type=' + type,
                'ext': {'fund_name': fund_name, 'type': type}
            })
        pg = response.meta['pg']
        t_count = json.loads(response.text.replace("'", "\""))['totalCount']
        tp = int(t_count)/8
        if pg < tp:
            pg += 1
            self.fps.append({
                'url': 'http://www.sywg.com/sywg/busiProduct.do?method=getProductProList&page={}'.format(pg),
                'pg': pg
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        type = response.meta['ext']['type']
        rows = re.search('netList:\[(.*?)\]', response.text).group(1)
        rows = rows.replace('\\', '')
        navs = re.findall('valueStr2:\'([0-9.]+)\'', rows)
        added_navs = re.findall('valueStr1:\'([0-9.]+)\'', rows)
        dates = re.findall('\d+-\d+-\d+', rows)
        for nav, added_nav, date in zip(navs, added_navs, dates):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = date
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            if type == '0':
                nav = nav
                item['nav'] = float(nav) if nav is not None else None
                annualized_return = added_nav
                item['added_nav'] = float(annualized_return) if annualized_return is not None else None
            else:
                nav = nav
                item['nav'] = float(nav) if nav is not None else None
                added_nav = added_nav
                item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

