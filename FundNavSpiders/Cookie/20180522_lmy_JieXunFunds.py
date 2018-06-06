# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-22

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class JieXunFundsSpider(GGFundNavSpider):
    name = 'FundNav_JieXunFunds'
    sitename = '杰询投资'
    channel = '投顾净值'
    allowed_domains = ['www.jxfunds.com']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'UM_distinctid=163053a583d4bc-02fbcaeafa98fa-454c092b-1fa400-163053a583e2c7; CNZZDATA1253653248=2039850130-1524800635-%7C1524904022; PHPSESSID=i0qclqkvlqd7t49l4517smq784; syCkE_auth=89331ws6vgtmgxBkfVx64nZTza5nweX2RCp2UbrbgSkI6YQIbsTgPG2ReBhRZsjxi1sOtYaNKkbYpF-bBBTctEQRI90h7Ja6qzMXwKBDZ2j-O_MyY1dP0RHyPDHnRdqkarFQOgEKTNln44o6SyxNXqAaCFc; syCkE__userid=89331ws6vgtmgxBkfVl84nVYza9ixOmkR3wnBbrd0Sk; syCkE__username=89331ws6vgtmgxBkfVp66XFWwK86x7TwEy0gAuK2ukMx3P4; syCkE__groupid=89331ws6vgtmgxBkfV4tvSUFxqFmlrf2Ryl_Bu3e; syCkE__nickname=89331ws6vgtmgxBkfVp66XFWwK86x7TwEy0gAuK2ukMx3P4'

    fps = [
        {'url': 'http://www.jxfunds.com/index.php?m=content&c=index&a=addpro&page1=0&catid=18&q=',
         'pg': 0},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath('//div[@class="list_mar2"]//a//@href').extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
            })

        if fund_urls:
            # 如果抓不到链接，则停止
            next_pg = response.meta['pg'] + 1
            self.fps.append({
                'url': 'http://www.jxfunds.com/index.php?m=content&c=index&a=addpro&page1=' + str(
                    next_pg) + '&catid=18&q=',
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        fund_name = response.xpath('//div[@class="main"]/div[2]/div[1]/p/text()').extract_first()
        nav_list = response.xpath('//div[@id="cat_2"]//table//tr')
        for row in nav_list[2:]:
            row_info = row.xpath('td//text()').extract()
            if len(row_info) >= 3:
                statistic_date = row_info[0]
                nav = row_info[2]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name.replace('【期限已到】', '').replace('【分红】', '')
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
                item['nav'] = float(nav) if nav is not None else None

                yield item
