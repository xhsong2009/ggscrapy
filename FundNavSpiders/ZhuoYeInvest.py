# -*- coding: utf-8 -*-

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ZhuoYeInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZhuoYeInvest'
    sitename = '卓晔投资'
    channel = '投资顾问'

    fps = [{
        'url': 'http://www.zhuoyetz.com/pr.jsp',
        'ref': 'http://www.zhuoyetz.com/'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//a[@class="fk-productName"]')
        for fund in funds:
            id = fund.xpath("./@href").extract_first()
            fund_name = fund.xpath("./text()").extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), id),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })
        # next_url = response.xpath("//a[contains(text(), '下一页')]/@href").extract_first()
        # if next_url is not None and next_url != response.url:
        #     self.ips.append({
        #         'url': next_url,
        #         'ref': response.url,
        #         'ext': {'fund_name': fund_name}
        #     })

    def parse_item(self, response):

        # 历史净值
        rows = response.xpath('//*[@id="detailedDesc"]/div/table[2]/tbody/tr')
        if len(rows) == 0:
            # 最新净值
            item = GGFundNavItem()
            fund_name = response.meta['ext']['fund_name']
            datas = response.xpath('//td[@class="propValue g_minor"]/span/text()').extract()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(datas[3], '%Y-%m-%d')
            item['nav'] = float(datas[2]) if datas[2] is not None else None
            item['added_nav'] = float(datas[1]) if datas[1] is not None else None

            yield item

        else:
            fund_name = response.xpath('//*[@id="detailedDesc"]/div/table[1]/tbody/tr[1]/td[2]/text()').extract_first()
            for row in rows[1:]:
                statistic_date = row.xpath('normalize-space(./td[1]/text())').extract_first()
                sign = statistic_date[4]
                statistic_date = datetime.strptime(statistic_date, '%Y' + sign + '%m' + sign + '%d')
                nav = row.xpath('normalize-space(./td[2]/text())').extract_first()
                added_nav = row.xpath('normalize-space(./td[3]/text())').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = statistic_date
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None

                yield item

