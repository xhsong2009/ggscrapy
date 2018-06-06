# -*- coding: utf-8 -*-

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ZheShangFuturesSpider(GGFundNavSpider):
    name = 'FundNav_ZheShangFutures'
    sitename = '浙商期货'
    channel = '期货净值'

    fps = [{
        'url': 'http://www.cnzsqh.com/Investors/List.aspx?ClassId=671&SubParentId=674&ParentId=127',
        'ref': 'http://www.cnzsqh.com/'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_dlNews"]//tr/td[2]/a')
        for fund in funds:
            statistic_date = fund.xpath("./text()").re_first('\d+-\d+-\d+')
            url = fund.xpath("./@href").extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url,
                'ext': {'statistic_date': statistic_date}
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@id="fontsize_6562"]//table/tbody/tr')[2:]
        statistic_date = response.meta['ext']['statistic_date']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = row.xpath('./td[2]/font/text()').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = row.xpath('./td[6]').re_first('>\s*([0-9.]+)\s*<')
            item['nav'] = float(nav) if nav is not None else None
            yield item
