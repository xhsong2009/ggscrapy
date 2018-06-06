# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WuKongAssetSpider(GGFundNavSpider):
    name = 'FundNav_WuKongAsset'
    sitename = '悟空投资'
    channel = '投顾净值'

    fps = [{'url': 'http://www.wukongtz.com/list/?6_1.html'}]

    def parse_fund(self, response):
        href_list = response.css('ul.f12 a::attr(href)').extract()
        for href in href_list:
            self.ips.append({
                'url': 'http://www.wukongtz.com%s' % href,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.css('tbody#result tr')
        for r in rows:
            fund_name = r.css('td:nth-child(1)::text').extract_first()
            date = r.css('td:nth-child(2)::text').extract_first()
            add_nav = r.css('td:nth-child(3) ::text').re_first("(.*)")

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            item['added_nav'] = float(add_nav) if add_nav else None
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None

            yield item

        next_href = response.xpath('//div[@class="pages"]//a[contains(text(),"下一页")]/@href').extract_first()
        if next_href:
            self.ips.append({
                'url': 'http://www.wukongtz.com/list/%s' % next_href,
                'ref': response.url
            })
