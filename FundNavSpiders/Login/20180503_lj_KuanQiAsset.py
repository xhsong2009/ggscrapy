# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-03

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
import time


class KuanQiAssetSpider(GGFundNavSpider):
    name = 'FundNav_KuanQiAsset'
    sitename = '宽奇资产'
    channel = '投资顾问'

    fps = [{'url': 'http://www.kuanqifund.com/157'}]

    username = 'zhangcheng'
    password = 'ZYYXSM123'

    def start_requests(self):
        yield FormRequest(url='http://www.kuanqifund.com/apply/member/userLogin.asp',
                          formdata={'userNameLogin': 'zhangcheng',
                                    'passwordLogin': '4b945bbfdea5a65abfea85e49d1558a8',
                                    'userLoginCheckcode': '7505',
                                    'userLabelId': '529'},
                          callback=self.parse_fund)

    def parse_fund(self, response):
        time.sleep(3)
        fund_infos = response.xpath('//div[@class="fwmain_nleft edit_putHere"]/div/div//span//h2[2]//a')
        for url in fund_infos:
            ips_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first().replace('产品净值（', '').replace('）', '')
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//table[@class='MsoNormalTable']/tbody//tr")
        fund_name = response.meta['ext']['fund_name']
        for row in rows[1:]:
            fund_date = row.xpath('.//td[1]/p//span[1]/text()').extract_first()
            fund_nav = row.xpath('.//td[2]/p//span[1]/text()').extract_first()
            if fund_date != '2016-10-':
                item = GGFundNavItem()

                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
                item['nav'] = float(fund_nav)
                yield item

