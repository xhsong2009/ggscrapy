# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HengChangInvestSpider(GGFundNavSpider):
    name = 'FundNav_HengChangInvest'
    sitename = '恒昌资产'
    channel = '投资顾问'
    allowed_domains = ['hengczb.bj2.lcweb01.cn']

    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [{'url': 'http://hengczb.bj2.lcweb01.cn/3g/index.php?p=jijin'}]

    def parse_item(self, response):
        rows = response.xpath("//article[@class='container news-article']//tr")
        for row in rows[1:]:
            fund_name = row.xpath('./td[1]//text()').extract_first()
            added_nav_info = row.xpath('./td[4]//text()').extract_first()
            if '已' not in added_nav_info:
                added_nav = added_nav_info.split('(')[0]
                statistic_date = '20' + added_nav_info.split('(')[1].replace(')', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y.%m.%d')
                yield item
