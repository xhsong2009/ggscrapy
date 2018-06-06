# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-04-27

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HaiZhongWanTouZiInvestInvestSpider(GGFundNavSpider):
    name = 'FundNav_HaiZhongWanTouZiInvest'
    sitename = '海中湾投资'
    channel = '投顾净值'

    fps = [{'url': 'http://www.sdhzwtz.cn/index.php?g=&m=article&a=index&id=61'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='main clear']/ul[@class='menu']/li//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.sdhzwtz.cn' + fund_url,
                'ref': response.url,
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='news_nr']//tr")
        for row in rows[1:]:
            fund_names = row.xpath("./td[1]//text()").extract()
            fund_name = ''.join(fund_names)
            date = row.xpath("./td[2]//text()").extract()
            statistic_date = ''.join(date)
            navs = row.xpath("./td[3]//text()").extract()
            nav = ''.join(navs)
            added_navs = row.xpath("./td[3]//text()").extract()
            added_nav = ''.join(added_navs)
            if nav:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
