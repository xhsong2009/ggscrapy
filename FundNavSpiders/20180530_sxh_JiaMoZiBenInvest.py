# -*- coding: utf-8 -*-
# Department：保障部
# Author：宋孝虎
# Create_Date：2018-05-30

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class JiaMoZiBenInvestSpider(GGFundNavSpider):
    name = 'FundNav_JiaMoZiBenInvest'
    sitename = '嘉谟资本'
    channel = '投顾净值'
    allowed_domains = ['www.gammacapital.com.cn']

    ips = [{
        'url': 'http://www.gammacapital.com.cn/?page_id=9&sk&order=unit_price&face=cont-products',
        'ref': 'http://www.gammacapital.com.cn'
    }]

    def parse_item(self, response):
        rows = response.xpath("//div[@class='con_prd_cate active']//tr")
        for row in rows[1:]:
            fund_name = row.xpath('./td[1]//text()').extract_first()
            nav = row.xpath('./td[3]//text()').extract_first()
            added_nav = row.xpath('./td[4]//text()').extract_first()
            statistic_date = row.xpath('./td[5]//text()').extract_first().replace('更新日期', '').replace(':', '').replace(
                '（届满结束）', '').strip()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            if fund_name == '嘉谟动量':
                item['statistic_date'] = datetime.strptime(statistic_date, '%d/%m/%Y')
            else:
                item['statistic_date'] = datetime.strptime(statistic_date, '%m/%d/%Y')
            yield item
