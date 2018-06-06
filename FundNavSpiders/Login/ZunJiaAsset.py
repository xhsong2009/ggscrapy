# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime

import lxml.etree
from scrapy import FormRequest

from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZunJiaAssetSpider(GGFundNavSpider):
    name = 'FundNav_ZunJiaAsset'
    sitename = '尊嘉资产'
    channel = '投顾净值'

    def start_requests(self):
        yield FormRequest(url='http://www.juniorchina.com.cn/Index/login_in.html',
                          formdata={
                              'name': '18939019964',
                              'pwd': '890621',
                              'checkSent': '0',
                              'value': 'ok'

                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps.append({
            'url': 'http://www.juniorchina.com.cn/Product/product.html',
            'ref': response.url
        })

    def parse_fund(self, response):
        funds = response.xpath('//ul[@id="xiala"]/li/p')
        ids = response.xpath('//ul[@id="xiala"]/script')
        for (fund, id) in zip(funds, ids):
            fund_name = fund.xpath('normalize-space(./text())').extract_first()
            fund_id = id.xpath('./text()').extract_first()
            fund_id = re.findall('\d+', fund_id)[1]
            self.ips.append({
                'url': 'http://www.juniorchina.com.cn/Product/juniorchina_produt.html?fund_id=' + fund_id,
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name, 'fund_id': fund_id}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        info_json = json.loads(response.text)
        chart = lxml.etree.HTML(info_json['content'])
        rows = chart.xpath('//table[@id="juniorchina_table"]/tr')
        for row in rows[1:]:
            statistic_date = row.xpath('./td[1]/text()')
            if len(statistic_date) == 0:
                continue
            statistic_date = statistic_date[0]
            nav = row.xpath('./td[2]/text()')[0]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        #总页数
        tp = chart.xpath('//script[contains(text(),"pagenumber")]/text()')[0]
        tp = re.findall('pagenumber"\)\.val\("(\d+)', tp)[0]
        pg = response.meta['pg']
        fund_id = response.meta['ext']['fund_id']
        if pg < int(tp):
            pg = pg+1
            self.ips.append({
                'url': 'http://www.juniorchina.com.cn/Product/juniorchina_produt.html?fund_id=' + fund_id + '&begin=&over=&new_page=' + str(pg),
                'ref': response.url,
                'pg': pg,
                'ext': {'fund_name': fund_name, 'fund_id': fund_id}
            })
