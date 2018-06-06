# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-02

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
import re


class HongYiTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HongYiTouZiInvest'
    sitename = '鸿逸投资'
    channel = '投顾净值'
    allowed_domains = ['www.hongyish.com.cn']
    username = '15838569960'
    password = 'm19890226'
    fps = [{'url': 'http://www.hongyish.com.cn/proindex.asp'}]

    def start_requests(self):
        yield FormRequest(url='http://www.hongyish.com.cn/MemberLogin.asp',
                          formdata={'LoginName': '15838569960',
                                    'LoginPass': 'm19890226',
                                    'x': '41',
                                    'y': '17',
                                    }
                          )

    def parse_fund(self, response):
        fund_urls = response.xpath("//td[@id='submenu1']//tr")
        for url in fund_urls:
            fund_url = url.xpath(".//@href").extract_first()
            fund_name = url.xpath("./td//text()").extract()[1]
            self.ips.append({
                'url': fund_url.replace('pro.asp?', 'http://www.hongyish.com.cn/equity.asp?page=1&'),
                'ref': response.url,
                'ext': {'fund_name': fund_name},
                'pg': 1
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//div[@class='bottombox fl']/table[@class='equityTable']//tr")
        end_pg = re.findall('当前为<font color="#FF0000">(.*?)</font>/(\d+)页 ', response.text)[0][1]
        if len(rows) > 1:
            for row in rows[1:]:
                statistic_date = row.xpath("./td[1]//text()").extract_first()
                nav = row.xpath("./td[2]//text()").extract_first()
                added_nav = row.xpath("./td[3]//text()").extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                yield item

        pg = response.meta['pg']
        if pg < int(end_pg):
            next_pg = pg + 1
            next_url = response.url.replace('?page=' + str(pg), '?page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })

