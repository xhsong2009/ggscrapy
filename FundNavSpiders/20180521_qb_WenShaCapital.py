# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WenShaCapitalSpider(GGFundNavSpider):
    name = 'FundNav_WenShaCapital'
    sitename = '温莎资本'
    channel = '投资顾问'

    fps = [{'url': 'http://www.windsorfund.cn/jingxuan9.html'}]

    def parse_fund(self, response):
        href_list = response.css('div.span4.menu-side a::attr(href)').extract()
        fname_list = response.css('div.span4.menu-side a::text').extract()
        for h, fname in zip(href_list, fname_list):
            if 'announcement' not in h:
                href = h.replace('./', '')
                self.ips.append({
                    'url': 'http://www.windsorfund.cn/' + href,
                    'ref': response.url,
                    'ext': fname,
                    'dont_retry': True,
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301, 302]
                })

    def parse_item(self, response):
        if response.status == 200:
            rows = response.xpath('//div[contains(@class,"product_tab_sub")][3]//tr')
            fund_name = response.meta['ext'].replace(':', '')
            for r in rows[1:]:
                date = r.css('td:nth-child(1)::text').re_first('\S+')
                add_nav = r.css('td:nth-child(2)::text').re_first('\S+')

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['added_nav'] = float(add_nav.replace(' ', '')) if add_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y/%m/%d') if date else None

                yield item
