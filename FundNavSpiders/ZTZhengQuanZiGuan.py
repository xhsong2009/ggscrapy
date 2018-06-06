# -*- coding: utf-8 -*-

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class ZTZhengQuanZiGuanSpider(GGFundNavSpider):
    name = 'FundNav_ZTZhengQuanZiGuan'
    sitename = '中天证券资管'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.iztzq.com/servlet/json',
        'ref': 'http://www.iztzq.com/',
        'form': {
            'funcNo': '834005',
            'curPage': '1',
            'numPerPage': '10',
            'proType': '4'
        }
    }, {
        'url': 'http://www.iztzq.com/servlet/json',
        'ref': 'http://www.iztzq.com/',
        'form': {
            'funcNo': '834005',
            'curPage': '1',
            'numPerPage': '10',
            'proType': '5'
        }
    }, {
        'url': 'http://www.iztzq.com/servlet/json',
        'ref': 'http://www.iztzq.com/',
        'form': {
            'funcNo': '834005',
            'curPage': '1',
            'numPerPage': '10',
            'proType': '6'
        }
    }, {
        'url': 'http://www.iztzq.com/servlet/json',
        'ref': 'http://www.iztzq.com/',
        'form': {
            'funcNo': '834005',
            'curPage': '1',
            'numPerPage': '10',
            'proType': '7'
        }
    }, {
        'url': 'http://www.iztzq.com/servlet/json',
        'ref': 'http://www.iztzq.com/',
        'form': {
            'funcNo': '834005',
            'curPage': '1',
            'numPerPage': '10',
            'proType': '8'
        }
    }
    ]

    def parse_fund(self, response):
        info_json = json.loads(response.text)
        datas = info_json['results'][0]['data']
        for data in datas:
            pro_code = data['pro_code']
            self.ips.append({
                'url': 'http://www.iztzq.com/servlet/json',
                'ref': response.url,
                'form': {
                    'funcNo': '834013',
                    'code': pro_code,
                    'page': '1',
                    'numPerPage': '10'
                },
                'ext': {'pro_code': pro_code}
            })

        # 总页数
        tp = info_json['results'][0]['totalPages']
        # 当前页
        cp = info_json['results'][0]['currentPage']
        if int(cp) < int(tp):
            cp = cp + 1
            self.fps.append({
                 'url': 'http://www.iztzq.com/servlet/json',
                 'ref': response.url,
                 'form': {
                     'funcNo': '834005',
                     'curPage': str(cp),
                     'numPerPage': '10',
                     'proType': response.meta['form']['proType']
                 }
            })

    def parse_item(self, response):
        info_json = json.loads(response.text)
        datas = info_json['results'][0]['data']
        for data in datas:
            fund_name = data['pro_name']
            nav = data['nav']
            add_nav = data['accumulativenav']
            statistic_date = data['tradedate']
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = statistic_date
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(add_nav) if add_nav is not None else None

            yield item

        # 总页数
        tp = info_json['results'][0]['totalPages']
        # 当前页
        cp = info_json['results'][0]['currentPage']
        pro_code = response.meta['ext']['pro_code']
        if int(cp) < int(tp):
            cp = cp+1
            self.ips.append({
                'url': 'http://www.iztzq.com/servlet/json',
                'ref': response.url,
                'form': {
                    'funcNo': '834013',
                    'code': pro_code,
                    'page': str(cp),
                    'numPerPage': '10'
                },
                'ext': {'pro_code': pro_code}
            })
