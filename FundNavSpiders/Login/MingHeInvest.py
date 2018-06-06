# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-06

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class MingHeInvestSpider(GGFundNavSpider):
    name = 'FundNav_MingHeInvest'
    sitename = '明河投资'
    channel = '投顾净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.river-fund.com/index.php?m=product&c=index&a=net&catid=1',
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.river-fund.com/index.php?m=users&c=index&a=login',
                          formdata={'id_number': self.username,
                                    'password': self.password,
                                    'type': 'browse'},
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [302, 301]
                          })

    def parse_fund(self, response):
        ips_list = response.css('div.aboutWarpShow div.warpLfMune a::attr(href)').extract()
        name_list = response.css('div.aboutWarpShow div.warpLfMune a::text').extract()
        for ips_url, f_name in zip(ips_list, name_list):
            self.ips.append({
                'url': ips_url + '&page=1',
                'ref': response.url,
                'pg': 1,
                'ext': f_name
            })

    def parse_item(self, response):
        rows = response.css('table.tableStyle.overvieTOP tr')[1:]
        if rows:
            for r in rows:
                row = r.xpath('td//text()').extract()
                date = row[1]
                nav = row[2]
                add_nav = row[3]
                fund_name = response.meta['ext']

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(add_nav) if add_nav is not None else None
                yield item

            next_pg = response.meta['pg'] + 1

            self.ips.append({
                'url': re.sub('\d+$', str(next_pg), response.url),
                'ref': response.url,
                'pg': next_pg,
                'ext': response.meta['ext']
            })
