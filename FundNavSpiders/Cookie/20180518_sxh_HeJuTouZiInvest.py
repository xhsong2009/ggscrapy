# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class HeJuTouZiiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HeJuTouZiiInvest'
    sitename = '和聚投资'
    channel = '投顾净值'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'JSESSIONID=3E6279CA6E1FFA89E14EA08CD565D6C9; acw_tc=AQAAACBIaQwaqwIA9bNuy6fteinTidPa; JSESSIONID=3E6279CA6E1FFA89E14EA08CD565D6C9; JSESSIONID=3E6279CA6E1FFA89E14EA08CD565D6C9; clientlanguage=zh_CN'

    fps = [{'url': 'https://www.hejufund.com/member/fundInfo/list.jspx'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@id='fundDayDiv']//tr")
        for url in fund_urls[1:]:
            fund_name = url.xpath('./td[2]//text()').extract_first()
            fund_url = url.xpath('./td[2]//@href').extract_first()
            self.ips.append({
                'url': 'https://www.hejufund.com/member/fundInfo/ferter_info.jspx?fundCode=' + fund_url.replace(
                    '/member/fundInfo/detail.jspx?fundCode=', '').replace('&q=', '') + '&pageIndex=1',
                'ref': response.url,
                'ext': {'fund_name': fund_name},
                'pg': 1
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = json.loads(response.text)['list']
        if rows:
            for row in rows:
                statistic_date = row['cDate']
                nav = row['netValue']
                added_nav = row['totalNetValue']
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            pg = response.meta['pg']
            next_pg = pg + 1
            next_url = response.url.replace('pageIndex=' + str(pg), 'pageIndex=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })
