# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-07

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import json


class HuaJingSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_HuaJingSecurities'
    sitename = '华菁证券资管'
    channel = '发行机构'

    fps = [{'url': 'https://am.huajingsec.com/netvalue/index.html',
            'ref': 'https://am.huajingsec.com/index.html'}]

    def parse_fund(self, response):
        name = response.xpath('//div[@class="selbody1 lmenu"]/ul/li/ul//li/a//text()').extract()
        product_id = re.findall('<li pcode="(.*?)" pname', response.text)
        for name, p_id in zip(name, product_id):
            fund_name = name
            fund_id = p_id
            ips_url = 'https://am.huajingsec.com/common-web/chart/fundnetchart!getFundNetChartJson?fundcode=' + fund_id + '&charttype=2'
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        data = json.loads(response.text)
        nav = data['seriesData0']
        added_nav = data['seriesData1']
        statistic_date = data['xAxisData']

        for nav, added_nav, statistic_date in zip(nav, added_nav, statistic_date):
            added_nav = float(added_nav)
            statistic_date = statistic_date

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
