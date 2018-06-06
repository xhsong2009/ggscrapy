# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-08

from datetime import datetime
from scrapy import FormRequest, Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class GoldenQuantSpider(GGFundNavSpider):
    name = 'FundNav_GoldenQuant'
    sitename = '灰金量投'
    channel = '投资顾问'

    username = '13916427906'
    password = 'ZYYXSM123'
    fps = [{'url': 'https://goldenquant.com'}]

    def start_requests(self):
        yield Request(url='https://goldenquant.com/login', callback=self.parse_login)

    def parse_login(self, response):
        token = response.xpath('//input[@name="_token"]/@value').extract_first()
        yield FormRequest(url='https://goldenquant.com/login',
                          method='POST',
                          formdata={'_token': token,
                                    'email': self.username,
                                    'password': self.password,
                                    'remember': '1'
                                    },
                          )

    def parse_fund(self, response):
        name_info = response.xpath(
            '//div[@class="col-sm-6 col-md-4 col-lg-3 text-center m-top-24"]/div[@class="investments-top"]/p[@class="title-lg opacity-1"]/text()').extract()
        code_info = response.xpath(
            '//div[@class="col-sm-6 col-md-4 col-lg-3 text-center m-top-24"]/div[@class="investments-bottom"]/a[@class="btn btn-orange btn-width-200"]/@onclick').re(
            '\d+')

        for name, code in zip(name_info, code_info):
            nav_link = 'https://goldenquant.com/api/product/' + code + '/nav'
            self.ips.append({
                'url': nav_link,
                'ref': response.url,
                'ext': name
            })

    def parse_item(self, response):
        nav_json = json.loads(response.text)

        for nav_info, added_nav_info in zip(nav_json['nav'], nav_json['auv']):
            nav = nav_info[1]
            added_nav = added_nav_info[1]
            statistic_date = datetime.fromtimestamp((nav_info[0] / 1000))
            fund_name = response.meta['ext']

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            item['statistic_date'] = statistic_date if statistic_date else None

            yield item
