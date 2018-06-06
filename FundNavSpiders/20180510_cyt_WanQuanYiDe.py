# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-10

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class WanQuanYiDeSpider(GGFundNavSpider):
    name = 'FundNav_WanQuanYiDe'
    sitename = '深圳万泉易德资产'
    channel = '投顾净值'
    allowed_domains = ['www.wqydzc.com']
    start_urls = ['http://www.wqydzc.com/qxcp/']

    fps = [{'url': 'http://www.wqydzc.com/qxcp/'}]

    def parse_fund(self, response):
        link_key = response.xpath('//div[@class="con"]/dl[@class="sort_brand"]/dt/a/@href').extract()
        for key in link_key:
            fund_link = urljoin('http://www.wqydzc.com', key)
            self.ips.append({
                'url': fund_link,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath('//tr[@class="tr01"][1]/td[2]/text()').extract_first()
        nav_rows = response.xpath('//table[@class="table01"]//tr')
        for row in nav_rows[1:]:
            nav_info = row.xpath('td/text()').extract()
            statistic_date = nav_info[0].strip()
            nav = nav_info[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d %H:%M:%S')
            item['nav'] = float(nav) if nav is not None else None

            yield item
