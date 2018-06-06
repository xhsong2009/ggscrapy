# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class PinJinZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_PinJinZiChanInvest'
    sitename = '品今资产'
    channel = '投顾净值'
    allowed_domains = ['www.chinapinjinamc.com']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    fps = [
        {'url': 'http://www.chinapinjinamc.com/index/project/product/page/1',
         'pg': 1}
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//ul[@class='product_online_list']/li//@href").extract()
        if fund_urls:
            for fund_url in fund_urls:
                self.ips.append({
                    'url': fund_url + '?moretable=1&pagedd=1',
                    'ref': response.url,
                    'pg': 1
                })
            pg = response.meta['pg']

            next_url = pg + 1
            self.fps.append({
                'url': 'http://www.chinapinjinamc.com/index/project/product/page/' + str(next_url),
                'ref': response.url,
                'pg': next_url
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='value_list value_list_fw clearfix']//tr")
        fund_name = response.xpath("//h1[@class='list_title clearfix']/span[@class='t']//text()").extract_first()
        statistic_title = response.xpath(
            "//div[@class='value_list value_list_fw clearfix']/table/thead/tr/th[7]//text()").extract_first()
        if len(rows) > 1:
            for row in rows[1:]:
                if statistic_title:
                    statistic_date = row.xpath("./td[7]//text()").extract_first().strip()
                else:
                    statistic_date = row.xpath("./td[4]//text()").extract_first().strip()
                nav = row.xpath("./td[2]//text()").extract_first()
                added_nav = row.xpath("./td[3]//text()").extract_first()
                if nav is not None:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['nav'] = float(nav)
                    if added_nav is not None:
                        item['added_nav'] = float(added_nav)
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                    yield item
            pg = response.meta['pg']
            next_pg = pg + 1
            self.ips.append({
                'url': response.url.replace('pagedd=' + str(pg), 'pagedd=' + str(next_pg)),
                'ref': response.url,
                'pg': next_pg,
            })
