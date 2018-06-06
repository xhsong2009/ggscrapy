# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
import json
import time


class NanHuaFuturesSpider(GGFundNavSpider):
    name = 'FundNav_NanHuaFutures'
    sitename = '南华期货'
    channel = '期货净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    stamp_href = 't=%s' % int(time.time() * 1000)
    fps = [{'url': 'https://www.nanhua.net/assetdata/all.json?' + stamp_href}]

    def start_requests(self):
        yield FormRequest(url='https://www.nanhua.net/member/newLogin.shtm?start=0&%s' % self.stamp_href,
                          formdata={'account': self.username,
                                    'password': self.password,
                                    'isagree': 'on',
                                    'rememberme': '1'
                                    })

    def parse_fund(self, response):
        data = json.loads(response.text)
        for i in data:
            code = i[0]
            self.ips.append({
                'url': 'https://www.nanhua.net/assetdata/%s.json?%s' % (code, self.stamp_href),
                'ref': response.url,
            })

    def parse_item(self, response):
        data = json.loads(response.text)
        for d in data:
            stamp = d[0]
            fund_name = d[1]
            nav = d[2]
            date = datetime.fromtimestamp(stamp / 1000)

            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = date
            item['nav'] = float(nav) if nav else None

            yield item
