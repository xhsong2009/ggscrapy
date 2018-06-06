from datetime import datetime
from scrapy import Request, FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class HangZhouMingXiAssetSpider(GGFundNavSpider):
    name = 'FundNav_HangZhouMingXiAsset'
    sitename = '杭州明曦资本'
    channel = '投资顾问'
    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    def start_requests(self):
        url = 'http://www.mingxifund.com/check'
        yield Request(url=url, callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.mingxifund.com',
                          formdata={'mingxi': ''},
                          method='POST',
                          callback=self.parse_next_login)

    def parse_next_login(self, response):
        url = 'http://www.mingxifund.com/signin/'
        yield FormRequest(url=url,
                          formdata={'name': self.username, 'pwd': self.password},
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps = [{
            'url': 'http://www.mingxifund.com/page-services.html#/CTA1',
            'ref': response.url
        }]

    def parse_fund(self, response):
        funds = response.xpath('/html/body/div/div[2]/div[@class="container-fluid"]/div/ul/li/a')
        for fund in funds:
            url = fund.xpath('./@href').extract_first()
            fund_name = fund.xpath('./text()').extract_first()
            fund_id = url[1:]
            url = 'http://www.mingxifund.com/get_data/'
            self.ips.append({
                'url': url,
                'form': {'pname': str(fund_id)},
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        rows = json.loads(response.text)
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            statistic_date = row['time']
            added_nav = row['net_value'] / 10000
            item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
