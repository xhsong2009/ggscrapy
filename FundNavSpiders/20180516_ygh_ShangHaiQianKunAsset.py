# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-16


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class ShangHaiQianKunAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiQianKunAsset'
    sitename = '上海乾堃资产'
    channel = '投资顾问'
    allowed_domains = ['www.qk-capital.com']

    ips = [{
        'url': 'http://www.qk-capital.com/lists/30/p/1.html',
    }]

    def parse_item(self, response):
        f_list = response.xpath('//tbody//tr')
        for i in f_list:
            item = GGFundNavItem()
            t = i.xpath('td//text()').extract()
            fund_name = re.findall('.*净值', t[0])[0].replace('净值', '')
            if i.xpath('td[3]//text()'):
                nav = t[1]
                added_nav = t[2]
                statistic_date = t[3]
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if nav is not None else None
            else:
                nav = t[1]
                statistic_date = t[2]
                item['nav'] = float(nav) if nav is not None else None

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date,'%Y-%m-%d')
            yield item

        next_href = response.xpath('//li[@class ="paging_next"]//a[contains(text(),下一页)]//@href').extract_first()
        if next_href:
            ips_url = 'http://www.qk-capital.com' + next_href
            self.ips.append({
                'url': ips_url,
                'ref': response.url
            })
