# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy import FormRequest


class QianHaiFangYuanInvestSpider(GGFundNavSpider):
    name = 'FundNav_QianHaiFangYuanInvest'
    sitename = '前海方圆资本'
    channel = '投顾净值'

    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.qhfyzb.com/content.asp?pid=3'}]

    def start_requests(self):
        yield FormRequest(url='http://www.qhfyzb.com/Plus/CheckLogin.asp',
                          formdata={'UserName': 'ZYYXSM',
                                    'UserPswd': 'ZYYXSM123',
                                    'verifycode': '',
                                    'input': '登录'},
                          )

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="pic_list"]/div//ul[@class="pic"]//@href').extract()
        fund_names = response.xpath('//div[@class="pic_list"]/div//ul[@class="pic"]//@alt').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.qhfyzb.com/', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="tab_ct jz"]/table//tr')
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            fund_date = row.xpath('.//td[3]//text()').extract_first()
            nav = row.xpath('.//td[4]//text()').extract_first()
            added_nav = row.xpath('.//td[6]//text()').extract_first()
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item
