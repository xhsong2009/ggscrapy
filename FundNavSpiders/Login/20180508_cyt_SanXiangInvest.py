# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-08

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class SanXiangInvestSpider(GGFundNavSpider):
    name = 'FundNav_SanXiangInvest'
    sitename = '惠州三想投资'
    channel = '投资顾问'

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.sanxianginvest.com/index.php?id=product'}]

    def start_requests(self):
        yield FormRequest(url='http://www.sanxianginvest.com/api.php?c=login&f=save&_noCache=0.8049219487167945',
                          headers={'Referer': 'http://www.sanxianginvest.com'},
                          formdata={
                              'post_date': '2025-05-08 16:00:43',
                              'pdip': '203.110.179.245',
                              'user': self.username,
                              'pass': self.password
                          })

    def parse_fund(self, response):
        name_list = response.xpath('//div[@class="product-list"]//tr/td[1]/a/text()').extract()
        fund_list = response.xpath('//div[@class="product-list"]//tr/td[1]/a/@href').extract()

        for fund_name, link in zip(name_list, fund_list):
            self.ips.append({
                'url': link,
                'ref': response.url,
                'ext': fund_name
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        nav_rows = response.xpath('//tr[@class="dd"]')

        for row in nav_rows:
            nav_info = row.xpath('td/text()').extract()
            statistic_date = nav_info[1].replace('25016-6-3', '2016-6-3').replace('.', '-').strip()
            nav = nav_info[2].strip()
            added_nav = nav_info[3].replace('..', '.').strip()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            yield item
