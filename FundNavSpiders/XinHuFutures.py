# -*- coding: utf-8 -*-

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import json


class XinHuFuturesSpider(GGFundNavSpider):
    name = 'FundNav_XinHuFutures'
    sitename = '新湖期货'
    channel = '期货净值'

    fps = [{
        'url': 'http://www.xinhu.cn/cfzx.html?action=list-more&page=1',
        'ref': 'http://www.xinhu.cn/'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//table[@class="tb-cfzx mgt10"]/tbody/tr/td[1]/a')
        for fund in funds:
            url = fund.xpath("./@href").extract_first()
            fund_name = fund.xpath("./text()").extract_first()
            self.ips.append({
                'url': url,
                'ref': response.url,
                'form': {
                    'curpage': '0',
                    'flag': ''
                },
                'ext': {'fund_name': fund_name}
            })
        next_url = response.xpath('//div[@class="pages"]/a[@class="next"]/@href').extract_first()
        if next_url is not None and next_url != '':
            self.fps.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        cur = response.meta['form']['curpage']
        if cur == '0':
            rows = response.xpath('//table[@id="trade_detail_table"]/tr')
            for row in rows[1:(len(rows)-1)]:
                statistic_date = row.xpath('normalize-space(./td[1]/text())').extract_first()
                if statistic_date is None or statistic_date == '':
                    continue
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                nav = row.xpath('normalize-space(./td[2]/text())').extract_first(default='')

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = statistic_date
                item['nav'] = float(nav) if nav is not None else None

                yield item
            # 总页数
            tp = response.xpath('//span[@class="qp_totalnumber"]/text()').extract()[0]
            # 当前页
            cp = response.xpath('//span[@class="qp_pagenumber"]/text()').extract()[0]
            if int(cp) < int(tp):
                next_url = response.url + '&dosubmit=1'
                self.ips.append({
                    'url': next_url,
                    'ref': response.url,
                    'form': {
                        'curpage': cp,
                        'flag': 'next'
                    },
                    'ext': {'fund_name': fund_name}
                })
        else:
            info_json = json.loads(response.text)
            rows = info_json['data']['list']
            for row in rows:
                if row is None:
                    break
                statistic_date = row['dateline']
                statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d')
                nav = row['total_nav']

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = statistic_date
                item['nav'] = float(nav) if nav is not None else None

                yield item

            # 总页数
            tp = info_json['data']['cpage']
            # 当前页
            cp = info_json['data']['page']
            if int(cp) < int(tp):
                next_url = response.url
                self.ips.append({
                    'url': next_url,
                    'ref': response.url,
                    'form': {
                        'curpage': str(cp),
                        'flag': 'next'
                    },
                    'ext': {'fund_name': fund_name}
                })
