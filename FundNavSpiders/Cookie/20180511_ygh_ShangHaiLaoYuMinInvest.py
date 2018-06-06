# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-11


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShangHaiLaoYuMinInvestSpider(GGFundNavSpider):
    name = 'FundNav_ygh_ShangHaiLaoYuMinInvest'
    sitename = '上海老渔民投资'
    channel = '投资顾问'
    allowed_domains = ['www.oldfisherman.cn']
    cookies = '__guid=184689711.2923636182507737000.1525937386563.4534; PHPSESSID=g7sv1g2vajam6i5n7tu6ho2j01; monitor_count=7'

    ips = [{
        'url': 'http://www.oldfisherman.cn/product.php',
    }]

    def parse_item(self, response):
        fund = response.xpath('//tbody//tr')
        for i in fund:
            t = i.xpath('td//text()').extract()
            if '产品名称' not in t[0]:
                item = GGFundNavItem()
                fund_name = t[0]
                statistic_date = t[1]
                nav = t[2]
                added_nav = t[3]
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if nav is not None else None
                yield item
