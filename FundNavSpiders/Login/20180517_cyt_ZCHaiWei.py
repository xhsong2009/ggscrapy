# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-17

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class ZCHaiWeiSpider(GGFundNavSpider):
    name = 'FundNav_ZCHaiWei'
    sitename = '深圳智诚海威资产'
    channel = '投顾净值'
    allowed_domains = ['www.bspartners.com.cn']
    start_urls = ['http://www.bspartners.com.cn/']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    fps = [{'url': 'http://www.bspartners.com.cn/'}]

    def start_requests(self):
        yield FormRequest(url='http://www.bspartners.com.cn/ajax/Login.aspx',
                          headers={'Referer': 'http://www.bspartners.com.cn/'},
                          formdata={
                              'FAction': 'login',
                              'Name': self.username,
                              'Pwd': self.password
                          })

    def parse_fund(self, response):
        fund_list = response.xpath('//ul[@class="dropdown-menu-next clearfix"][1]/li/a/@href').extract()
        for key in fund_list:
            fund_url = urljoin('http://www.bspartners.com.cn', key)
            self.ips.append({
                'url': fund_url,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath(
            '//div[@class="table-box"][1]/table[@class="table-pro"][1]//tr[1]/td[@class ="table-r"]/text()').extract_first()
        nav_rows = response.xpath('//div[@class="table-box"][2]/table[@class="table-trust-th"][1]//tr')

        for row in nav_rows[1:]:
            nav_info = row.xpath('td/text()').extract()
            statistic_date = nav_info[0].strip()
            nav = nav_info[1].strip()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None

            yield item
