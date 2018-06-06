# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 王卓诚
# Create_date : 2018-05-15

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class JinBaiRongInvestSpider(GGFundNavSpider):
    name = 'FundNav_JinBaiRongInvest'
    sitename = '金百镕投资'
    channel = '投顾净值'
    allowed_domains = ['www.gblcapital.com']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.gblcapital.com/index.php/product'
    }]

    def parse_fund(self, response):
        arul = response.xpath('//div[@class="left_side"]/ul/li')
        for uu in arul:
            pname = uu.xpath('a/text()').extract_first()
            pname = pname.replace('- ', '')
            url = uu.xpath('a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': pname
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        rows = response.xpath('//div[@id="fadecon"]/div[2]/table//table/tr')[1:]
        for k, row in enumerate(rows):
            statistic_date = row.xpath("./td[2]/text()").extract_first()
            nav = row.xpath("./td[3]/text()").extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item


