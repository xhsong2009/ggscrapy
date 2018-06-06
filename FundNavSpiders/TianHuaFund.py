# -*- coding: utf-8 -*-

import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class TianHuaFundSpider(GGFundNavSpider):
    name = 'FundNav_TianHuaFund'
    sitename = '杭州添华投资'
    channel = '投资顾问'

    fps = [
        {
            'url': 'http://www.tianhuafund.com/show-67-41-1.html'
        }
    ]

    def parse_fund(self, response):
        fund_name = response.xpath('//ul[@class="factor"]/li[1]/span/text()').extract_first()
        pro_id = response.xpath('//div[@class="list_boxL"]/ul/li[1]/a/@href').re_first(r'show-67-([\d]+)-1.html')
        self.ips.append({
            'url': 'http://www.tianhuafund.com/ajax_do.php?action=pages',
            'ref': response.url,
            'form': {'pageNum': '0', 'pro_id': pro_id},
            'pg': 0,
            'ext': {'fund_name': fund_name, 'pro_id': pro_id}
        })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        pro_id = ext['pro_id']
        json_data = json.loads(response.text)
        rows = json_data['list']
        for row in rows:
            statistic_date = row['date']
            nav = row['networth']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d') if len(statistic_date.split('/')) == 3 else datetime.strptime(statistic_date, '%Y/%m%d')
            item['nav'] = float(nav) if nav is not None else None
            yield item

        pg = response.meta['pg'] + 1
        tp = int(json_data['totalPage'])
        if pg < tp:
            self.ips.append({
                'url': 'http://www.tianhuafund.com/ajax_do.php?action=pages',
                'ref': response.url,
                'form': {'pageNum': str(pg), 'pro_id': pro_id},
                'pg': pg,
                'ext': {'fund_name': fund_name, 'pro_id': pro_id}
            })
