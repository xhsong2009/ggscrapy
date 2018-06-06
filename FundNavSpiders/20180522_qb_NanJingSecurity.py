# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-22

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
import re


class NanJingSecuritySpider(GGFundNavSpider):
    name = 'FundNav_NanJingSecurity'
    sitename = '南京证券'
    channel = '券商资管净值'

    trs_keycode = [13, 14, 15, 16, 17, 19, 24]
    ips = []
    for k in trs_keycode:
        href = 'productId=%s&current_page=1&pageSize=300' % k
        ips.append({
            'url': 'http://klyg.njzq.cn/iphone/callback/zg/include_cpjz.jsp?' + href,
            'pg': 1,
        })

    def parse_item(self, response):
        if 'null()' not in response.text:
            json_data = re.findall('null\((.*)\)', response.text, re.DOTALL)
            data = json.loads(json_data[0])['values']
            for d in data:
                fname = d['productName']
                date = d['netValueDateString']
                nav = d['strProductNetValue']
                add_nav = d['strCumulateNetValue']

                item = GGFundNavItem()
                if 'productId=17' in response.url:
                    item['sitename'] = self.sitename
                    item['fund_name'] = fname
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['annualized_return'] = float(nav.replace('．', '.')) if nav else None
                    item['d7_annualized_return'] = float(add_nav.replace(' ', '')) if add_nav else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item
                    continue

                item['sitename'] = self.sitename
                item['fund_name'] = fname
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav.replace('．', '.')) if nav else None
                item['added_nav'] = float(add_nav.replace(' ', '')) if add_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None

                yield item

            next_pg = response.meta['pg'] + 1
            next_url = re.sub('current_page=\d+', 'current_page=' + str(next_pg), response.url)
            self.ips.append({
                'url': next_url,
                'pg': next_pg,
            })
