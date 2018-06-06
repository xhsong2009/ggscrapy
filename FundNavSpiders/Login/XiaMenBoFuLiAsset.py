from datetime import datetime
from scrapy import Request,FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import json
import hashlib


class XiaMenBoFuLiAssetSpider(GGFundNavSpider):
    name = 'FundNav_XiaMenBoFuLiAsset'
    sitename = '厦门博孚利资产'
    channel = '投资顾问'
    username = '15618207420'
    password = '123456'
    cookies = 'isAgreen=1'

    def start_requests(self):
        yield Request(url='http://www.xmpfl.com', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        url = 'http://www.xmpfl.com/api/login'
        yield FormRequest(url=url,
                          formdata={'username': self.username, 'password': hashlib.md5(self.password.encode(encoding='UTF-8')).hexdigest()},
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps = [{
            'url': 'http://www.xmpfl.com/products/',
            'ref': response.url
        }]

    def parse_fund(self, response):
        funds = response.xpath('/html/body/div[3]//div[@class="bd"]/ul/li/a')
        for fund in funds:
            url = fund.xpath('./@href').extract_first()
            fund_name = fund.xpath('./text()').extract_first()
            fund_id = re.search(r'products\/(\d+)\.html', url).group(1)
            url = 'http://www.xmpfl.com/api/worth?id=' + fund_id
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        if response.status == 500:
            return
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        rows = json.loads(response.text)
        if rows:
            acc_values = rows['acc_values']
            dates = rows['date']
            values = rows['values']
            for date in dates:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                statistic_date = date
                nav = values.pop(0)
                added_nav = acc_values.pop(0)
                item['nav'] = float(nav) if nav is not None and nav != '' else None
                item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
