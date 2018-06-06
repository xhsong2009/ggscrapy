# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-06

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class MingDaAseetSpider(GGFundNavSpider):
    name = 'FundNav_MingDaAseet'
    sitename = '明达资产'
    channel = '投顾净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.mingdafund.com/index.php?controller=products&action=read&id=1',
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.mingdafund.com/index.php?controller=clientUsers&action=login',
                          formdata={'username': self.username,
                                    'password': self.password,
                                    'Submit': '登 录'},
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [302, 301]
                          })

    def parse_fund(self, response):
        id_list = response.xpath('//table[@width="180"]//td[@class="ldh"]//@href').re('action=read&id=(.*)')
        name_list = response.xpath('//table[@width="180"]//td[@class="ldh"]//text()').extract()
        for f_id, f_name in zip(id_list, name_list):
            self.ips.append({
                'url': 'http://www.mingdafund.com/index.php?controller=products&action=nets&id={}&type=1&page=0'.format(
                    f_id),
                'ref': response.url,
                'pg': 0,
                'ext': f_name
            })

    def parse_item(self, response):
        next_pg = response.meta['pg'] + 1
        total_pg = response.css('div#paper strong::text').extract()[1]
        if next_pg <= int(total_pg):
            rows = response.xpath('//td[@align="left"]//tr')[1:]
            for r in rows:
                if len(r.xpath('td')) > 1:
                    row = r.xpath('td//text()').extract()
                    date = row[0]
                    nav = row[1]
                    fund_name = response.meta['ext']

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                    item['nav'] = float(nav) if nav is not None else None
                    yield item

            self.ips.append({
                'url': re.sub('\d+$', str(next_pg), response.url),
                'ref': response.url,
                'pg': next_pg,
                'ext': response.meta['ext']
            })
