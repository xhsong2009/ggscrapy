# -*- coding: utf-8 -*-
# Department：保障部
# Author：王卓诚
# Create_Date：2018-05-25
from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
# from scrapy.utils.response import get_base_url
# from urllib.parse import urljoin
# from urllib.parse import urljoin
from scrapy import FormRequest
import json


class YingWeiInvestSpider(GGFundNavSpider):
    name = 'FundNav_YingWeiInvest'
    sitename = '惟盈投资'
    channel = '投顾净值'
    allowed_domains = ['www.winingfund.com']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.winingfund.com/index.php',
        'ref': 'http://www.winingfund.com'
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.winingfund.com/portals/login.php?p=wyzx2',
                          formdata={
                              'username': self.username,
                              'password': self.password
                          })

    def parse_fund(self, response):
        arul = response.xpath('//ul[@class="dropdown-menu"]/li')

        for uu in arul:
            url = uu.xpath('a/@href').extract_first()
            url = url.replace('portals/product.php?p=', '')
            if (not url.find('portals/') > -1):
                url2 = 'http://www.winingfund.com/portals/api.php?callback=jQuery2140059739919985194234_1526870154121&command=2001&product=' + url + '&_=1526870154122'
                self.ips.append({
                    'url': url2,
                    'ref': response.url
                })

    def parse_item(self, response):
        fund_info = response.text
        wz1 = fund_info.find('{"result')
        fund_info1 = fund_info[wz1:len(fund_info) - 1]
        fund_info2 = json.loads(fund_info1)
        productname_bf = fund_info2['result']['name']
        for k, v in enumerate(fund_info2['result']['date']):
            statistic_date = v
            nav = fund_info2['result']['value'][k]
            statistic_date = statistic_date.replace('/', '-')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = productname_bf
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav else None
            yield item
