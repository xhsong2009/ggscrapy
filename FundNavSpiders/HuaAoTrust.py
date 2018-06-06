# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-02

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HuaAoTrustSpider(GGFundNavSpider):
    name = 'FundNav_HuaAoTrust'
    sitename = '华澳信托'
    channel = '信托净值'

    fps = [{
        'url': 'http://www.huaao-trust.com/list/705/1.shtml',
        'pg': 1
    }]

    def parse_fund(self, response):
        href_list = response.css('div.news_list a::attr(href)').extract()
        if href_list:
            for href in href_list:
                self.ips.append({
                    'url': urljoin(get_base_url(response), href),
                    'ref': response.url

                })

            next_pg = response.meta['pg'] + 1
            self.fps.append({
                'url': 'http://www.huaao-trust.com/list/705/%s.shtml' % next_pg,
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        rows = response.css('div.news_details tr')
        for r in rows[1:]:
            row = r.xpath('td//text()').extract()
            fund_name = row[0]
            fund_date = row[2]
            fund_nav = row[3]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y/%m/%d')
            item['nav'] = float(fund_nav) if fund_nav else None
            yield item
