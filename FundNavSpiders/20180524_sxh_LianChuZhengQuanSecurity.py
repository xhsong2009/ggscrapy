# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-24


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class LianChuZhengQuanSecutiesSpider(GGFundNavSpider):
    name = 'FundNav_LianChuZhengQuanSecuties'
    sitename = '联储证券'
    channel = '券商资管净值'
    allowed_domains = ['mall.lczq.com']
    urername = '1499341527@qq.com'
    password = 'ZYYXSM123'

    def start_requests(self):
        ids = ['257', '258', '259', '260', '262', '263', '264', '265', '266', '267', '268', '269', '276', '277', '278',
               '279', '280', '282', '283', '284', '285', '286', '287', '288', '289', '324', '326', '327', '328', '331',
               '334', '335', '336', '337', '338', '341', '342', '343', '344', '345', '346', '347', '348', '349', '350',
               '351', '352', '353', '354', '355', '356', '359', '360', '361', '363', '366', '369', '370', '372', '374',
               '375', '377', '378', '379']
        for id in ids:
            self.ips.append({
                'url': 'https://mall.lczq.com/servlet/json?funcNo=1000071&product_id=' + id + '&start_date=&end_date=&curPage=1&numPerPage=1000',
                'ref': 'https://mall.lczq.com/servlet/',
            })
        yield self.request_next()

    def parse_item(self, response):
        row_info = json.loads(response.text)
        rows = row_info['results'][0]['data']
        for row in rows:
            fund_name = row['product_name']
            statistic_date = row['nav_date'].replace('-', '')
            nav = row['relate_price']
            added_nav = row['cumulative_net']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
            yield item
