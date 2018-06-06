# -*- coding: utf-8 -*-
# Department：保障部
# Author：王卓诚
# Create_Date：2018-05-28

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class JinYuanSecuritySpider(GGFundNavSpider):
    name = 'FundNav_JinYuanSecurity'
    sitename = '金元证券'
    channel = '券商资管净值'
    allowed_domains = ['www.jyzq.cn']
    cookies = 'JSESSIONID=abcZWIrFf_HAH5unRYfow; loginumber=0.91299219250646320180522132951; _isLoginIn=83@%7C@%7C@1526967043614; user_id=83; nick_name=%E6%9C%9D%E6%9C%9D; userid=0b36ba4b8309331b123cc76bcf2915bc; ismechanism=0; isAccordWith=; url='
    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.jyzq.cn/servlet/json',
        'ref': 'http://www.jyzq.cn',
        'form': {'funcNo': '502001',
                 'pageNum': '1',
                 'pageSize': '100',
                 'i_product_small_type': '1',
                 'i_product_stat': '0'
                 }
    }]

    def parse_fund(self, response):
        fundnames = json.loads(response.text)
        fundnames1 = fundnames['results'][0]['data']
        for v1 in fundnames1:
            self.ips.append({
                'url': 'http://www.jyzq.cn/servlet/json',
                'ref': response.url,
                'pg': 1,
                'ext': v1['i_product_id'],
                'form': {
                    'funcNo': '501020',
                    'pageNum': '1',
                    'pageSize': '200',
                    'product_id': v1['i_product_id']
                }
            })

    def parse_item(self, response):
        pid = response.meta['ext']
        fund_info1 = json.loads(response.text)
        fund_into = fund_info1['results'][0]['data']

        for v in fund_into:
            pnamef = v['i_product_name']
            statistic_date = v['n_product_nav_day']
            nav = v['n_product_nav']
            added_nav = v['n_product_total_nav']
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = pnamef
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        if len(fund_into) > 2:
            next_pg = response.meta['pg'] + 1
            self.ips.append({
                'url': 'http://www.jyzq.cn/servlet/json',
                'ref': response.url,
                'pg': next_pg,
                'ext': pid,
                'form': {
                    'funcNo': '501020',
                    'pageNum': str(next_pg),
                    'pageSize': '200',
                    'product_id': pid
                }
            })
