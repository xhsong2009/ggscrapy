# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class GanTanHaoTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_GanTanHaoTouZi'
    sitename = '上海感叹号投资'
    channel = '投资顾问'
    allowed_domains = ['www.gthfund.com']

    fps = [{'url': 'http://www.gthfund.com/wp-content/themes/dux/action/proddetailhandler.php'}]

    def parse_fund(self, response):
        data = json.loads(response.text)
        fid_list = data['cps']
        for i in fid_list:
            fund_id = i['id']
            fund_name = i['prod']
            self.ips.append({
                'url': 'http://www.gthfund.com/wp-content/themes/dux/action/data.php?id=' + fund_id + '&page=1&calc=0',
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        nav_infos = json.loads(response.text)
        rows = nav_infos['data']
        fund_name = response.meta['ext']['fund_name']
        for row in rows:
            statistic_date = row['modtime']
            nav = row['nav']
            added_nav = row['netnav']
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
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
                'ext': {'fund_name': fund_name},
            })
