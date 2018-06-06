# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-04-25

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class GuoMinXinTuoTrustsSpider(GGFundNavSpider):
    name = 'FundNav_GuoMinXinTuoTrusts'
    sitename = '国民信托'
    channel = '信托净值'

    fps = [
        {'url': 'http://www.natrust.cn/fe/equity/catList.gsp'},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath(
            "//div[@class='job_list']/ul[@class='job_list_text job_list_text2']//li[1]//@href").extract()
        for url in fund_urls:
            self.ips.append({
                'url': 'http://www.natrust.cn/fe/equity/' + url + '&page=1',
                'ref': response.url,
                'pg': 1
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='Details_right']/div[@class='jz_table']//tr")
        fund_name = response.xpath("//div[@class='left']//text()").extract_first()
        if len(rows) > 1:
            for row in rows[1:]:
                statistic_date = row.xpath("./td[1]//text()").extract_first()
                if '-' in statistic_date:
                    statistic_date = statistic_date.replace('-', '/')
                if statistic_date[4] != '/':
                    statistic_date = statistic_date.replace(statistic_date[0:4], statistic_date[0:4] + '/')

                nav = row.xpath('./td[2]//text()').extract_first()
                added_nav = row.xpath('./td[3]//text()').extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                yield item

            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('&page=' + str(pg), '&page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
            })
