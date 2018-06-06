# -*- coding: utf-8 -*-
# Department：保障部
# Author：宋孝虎
# Create_Date：2018-05-30

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ChuanCaiZhengQuanSecuritySpider(GGFundNavSpider):
    name = 'FundNav_ChuanCaiZhengQuanSecurity'
    sitename = '川财证券'
    channel = '券商资管净值'
    allowed_domains = ['www.cczq.com']

    ips = [{
        'url': 'http://www.cczq.com/cgi-bin/NVFundAction?function=NVFundInfo&curPage=1&numPerPage=10&totalpage=23',
        'ref': 'http://www.cczq.com'
    }]

    def parse_item(self, response):
        rows = response.xpath('//tr')
        for row in rows[1:]:
            fund_name = row.xpath('./td[1]//text()').extract_first()
            statistic_date = row.xpath('./td[4]//text()').extract_first()
            nav = row.xpath('./td[2]//text()').extract_first()
            added_nav = row.xpath('./td[3]//text()').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
