# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-04-27

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import json


class HongYeQiHuoFuturesSpider(GGFundNavSpider):
    name = 'FundNav_HongYeQiHuoFutures'
    sitename = '弘业期货'
    channel = '期货净值'

    fps = [{'url': 'http://www.ftol.com.cn/main/lczx/zcgl/cpjzpl/detail.shtml'}]

    def parse_fund(self, response):
        fund_ids = re.findall(r'product_code="(.*?)"', response.text)
        for fund_id in fund_ids:
            self.ips.append({
                'url': 'http://www.ftol.com.cn/servlet/json?funcNo=906329&product_code=' + fund_id + '&year=0&month=3&day=0&_catalogId=&rightId=',
                'ref': response.url,
            })

    def parse_item(self, response):
        nav_intos = json.loads(response.text)
        nav_into = nav_intos['results'][0]
        fund_name = nav_into['product_shortname']
        nav_datas = nav_into['nav_date']
        navs = nav_into['product_nav_arr']

        for row in zip(nav_datas, navs):
            statistic_date = row[0]
            nav = row[1]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
