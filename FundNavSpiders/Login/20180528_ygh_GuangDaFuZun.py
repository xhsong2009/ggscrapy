# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-28


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request, FormRequest


class GuangDaFuZunSpider(GGFundNavSpider):
    name = 'FundNav_GuangDaFuZun'
    sitename = '光大富尊'
    channel = '投资顾问'
    username = '15838569960'
    password = 'm19890226'

    ips = [
        {'url': 'http://www.ebfortune.com/product/navlist/SE9010?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/2?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/3?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/S29403?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SE4114?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SE5274?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SE5276?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SE5749?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SE9027?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SK2137?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SK2138?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/SK2139?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/TG0004?p=1', 'pg': '1'},
        {'url': 'http://www.ebfortune.com/product/navlist/1?p=1', 'pg': '1'},
    ]

    def start_requests(self):
        yield Request(url='http://www.ebfortune.com/login?goto=http%3A%2F%2Fwww.ebfortune.com%2Fproduct%2Fnavlist%2FSE9010%3Fp%3D1',
                      callback=self.parse_login)

    def parse_login(self, response):
        token = response.xpath('//input[@name="puff_beetl_client_token"]/@value').extract_first()
        yield FormRequest(url='http://www.ebfortune.com/user/login',
                          formdata={'certificationtype': 'A', 'certificationnum': '15838569960',
                                    'password': '3282CE68ECE65435F13D05F4DCF5B0EB'},
                          headers={'Puff-ClientToken': token, 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})

    def parse_item(self, response):
        pg = response.meta['pg']
        f_list = response.xpath('//tr')
        for i in f_list[1:]:
            t = i.xpath('td//text()').extract()
            fund_name = t[0]
            statistic_date = t[1]
            nav = t[2]
            added_nav = t[3]
            item = GGFundNavItem()
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        if len(f_list) > 1:
            next_pg = int(pg) + 1
            self.ips.append({
                'url': response.url.split('=')[0] + '=' + str(next_pg),
                'ref': response.url,
                'pg': next_pg
            })
