# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-03

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class JiuXuZiChanSpider(GGFundNavSpider):
    name = 'FundNav_JiuXuZiChan'
    sitename = '九旭资产'
    channel = '投顾净值'

    fps = [{
        'url': 'http://www.jiuxuzc.com/',
        'ref': 'http://www.jiuxuzc.com/qixiachanpin/jiuxu2hao/2016-04-13/86.html'
    }]

    def parse_fund(self, response):
        fund_infos = response.xpath('//div[@class="jiuxu_nav"]/ul/li[3]/ul//li')
        for url in fund_infos:
            fund_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first()
            ips_url = urljoin('http://www.jiuxuzc.com/', fund_url)
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        funds = response.xpath("//div[@id='jx_chart']//tr")
        if funds:
            fund_name = funds[1].xpath('./td//text()').extract_first()
            added_nav = funds[3].xpath('./td//text()').extract()
            fund_date = funds[5].xpath('./td//text()').extract()
            nav = funds[2].xpath('./td/text()').extract()

            for i in zip(added_nav, fund_date, nav):
                added_nav = i[0]
                statistic_date = i[1]
                nav = i[2]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

