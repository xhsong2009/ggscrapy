# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 王卓诚
# Create_date : 2018-05-15

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
import time


class FuTengInvestSpider(GGFundNavSpider):
    name = 'FundNav_FuTengInvest'
    sitename = '富腾资产'
    channel = '投资顾问'
    allowed_domains = ['www.futeng.com']

    username = '13916427906'
    password = 'ZYYXSM123'
    fps = [{
        'url': 'http://www.futeng.com/futeng/front/jjcp'
    }]

    def parse_fund(self, response):
        urls = response.xpath('//table[@class="tabstyle"]/tr')
        for uu in urls:
            url1 = uu.xpath("td[2]/a/@href").extract_first()
            cpid = url1.replace('/futeng/front/toValueInfo?cpId=', '')
            pg = 0

            formdata = {
                'rowPerPage': '100',
                'pageNo': str(pg),
                'cpId': cpid
            }
            self.ips.append({
                'url': 'http://www.futeng.com/futeng/front/loadValueInfo',
                'form': formdata,
                'ext': cpid,
                'pg': 1
            })

    def parse_item(self, response):
        cpId = response.meta['ext']
        pg = response.meta['pg']
        fund_info = json.loads(response.text)

        if len(fund_info['data']) > 0:
            for k, v in enumerate(fund_info['data']):
                productname_bf1 = v['cpName']
                productname_bf1 = productname_bf1.strip()

                nav = v['cpjz']
                added_nav = v['cpljjz']
                statistic_date1 = (v['createTime']['time']) / 1000
                timearray = time.localtime(statistic_date1)
                statistic_date = time.strftime("%Y-%m-%d", timearray)
                nav = nav.strip()
                added_nav = added_nav.strip()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = productname_bf1
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                yield item

        if fund_info['totalCount'] > 0:
            next_pg = pg + 1
            formdata = {
                'rowPerPage': '100',
                'pageNo': str(next_pg),
                'cpId': cpId
            }
            self.ips.append({
                'url': "http://www.futeng.com/futeng/front/loadValueInfo",
                'ext': cpId,
                'form': formdata,
                'pg': next_pg

            })
