# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib import parse
import re


class KindoAssetSpider(GGFundNavSpider):
    name = 'FundNav_KindoAsset'
    sitename = '津渡资产'
    channel = '投资顾问'
    allowed_domains = ['http://www.kindoasset.com/']

    fps = [{'url': 'http://www.kindoasset.com/products.asp', }]

    def parse_fund(self, response):
        fund_infos = response.xpath('//div[@id="box_l"]/ul/li/a')
        for url in fund_infos:
            fund_name = url.xpath('.//text()').extract_first()
            conditionarr = parse.quote(fund_name)
            ips_url = 'http://www.kindoasset.com/products.asp?bclasscode=' + conditionarr + '&sclasscode=' + '&page=1'
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'pg': 1,
                'ext': {
                    'fund_name': fund_name
                }
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//div[@class="pro_con_b"][@id="con04"]/table//tr')
        if rows:
            for row in rows[2:]:
                statistic_date = row.xpath('.//td[1]//text()').extract_first()
                nav = row.xpath('.//td[2]//text()').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

            tpg = re.findall('<option selected="selected" value="value" >(.*?)/(.*?)</option>', response.text)[0][1]
            pg = response.meta['pg']
            old_str = 'page=' + str(pg)
            if pg < int(tpg):
                new_str = 'page=' + str(pg + 1)
                next_url = response.url.replace(old_str, new_str)
                self.ips.append({
                    'url': next_url,
                    'ref': response.url,
                    'pg': pg + 1,
                    'ext': {'fund_name': fund_name}
                })
