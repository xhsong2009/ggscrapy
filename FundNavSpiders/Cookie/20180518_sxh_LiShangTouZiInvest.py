# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import time


class LiShangTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_LiShangTouZiInvest'
    sitename = '理尚投资'
    channel = '投顾净值'
    allowed_domains = ['www.hzlishang.com']

    username = '1499341527@qq.com'
    password = 'ZYYXSM123'

    cookies = 'ASP.NET_SessionId=icelrswtv1a5vvrxynnglyur; lishang=userid=116&username=%e9%99%88%e7%84%95%e7%84%95'
    fps = [{'url': 'http://www.hzlishang.com/product.aspx?id=446'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("///div[@class='biao1']//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.hzlishang.com/' + fund_url,
                'ref': response.url,
            })

    def parse_item(self, response):
        fund_name = response.xpath("//div[@class='content2 fr']/h2//text()").extract_first().strip()
        rows = response.xpath("//table/tbody//tr")
        for row1 in rows:
            row = row1.xpath('./td').extract()
            if len(row) == 4:
                navs = row1.xpath('./td[1]//text()').extract()
                nav = ''.join(navs).strip()
                added_navs = row1.xpath('./td[2]//text()').extract()
                added_nav = ''.join(added_navs).strip()
                statistic_dates = row1.xpath('./td[4]//text()').extract()
                statistic_date = ''.join(statistic_dates).strip()
                try:
                    time.strptime(statistic_date, "%Y-%m-%d")
                    a = '正确'
                except:
                    a = '失败'

                if a == '正确':
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['nav'] = float(nav) if nav is not None else None
                    item['added_nav'] = float(added_nav) if nav is not None else None
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                    yield item
