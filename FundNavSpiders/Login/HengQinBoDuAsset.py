# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class HengQinBoDuAssetSpider(GGFundNavSpider):
    name = 'FundNav_HengQinBoDuAsset'
    sitename = '博度资产'
    channel = '投资顾问'

    username = '18603799126'
    password = '123456'

    def start_requests(self):
        yield FormRequest(url='http://www.broadmeasure.com/ChkLogin.asp',
                          formdata={'UserName': '18603799126', 'Password': '123456'},
                          callback=self.parse_login)

    def parse_login(self, response):
        urls = response.xpath('//div[@id="panel-element-506907"]/div/a/@href').extract()
        for url in urls:
            if url.find('#') != -1:
                url = 'pro.asp'
            self.fps.append({
                'url': 'http://www.broadmeasure.com/' + url,
                'ref': response.url
            })

    def parse_fund(self, response):
        fund_name = response.xpath('normalize-space(//div[@id="ys"]/table/tbody/tr[1]/td[2]/text())').extract_first()
        self.ips = [{
            'url': 'http://www.broadmeasure.com/datetab.php',
            'ref': response.url,
            'ext': {'fund_name': fund_name}
        }]

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        info_json = json.loads(response.text)
        rows = info_json['dataList']
        for row in rows:
            statistic_date = row['datelist']
            added_nav = row['val']
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

