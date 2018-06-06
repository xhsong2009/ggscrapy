# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-08

from datetime import datetime
from scrapy import FormRequest, Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class NaSiTeInvestSpider(GGFundNavSpider):
    name = 'FundNav_NaSiTeInvest'
    sitename = '纳斯特'
    channel = '投顾净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.gfnest.com/pm/productinformation_doFindProductins.do?code=product'}]

    def start_requests(self):
        yield FormRequest(url='http://www.gfnest.com/customers/cust_doLogin.do',
                          formdata={
                              'cust.cusiName': '13916427906',
                              'cust.cusiPassword': 'A80DC5E79C03C9AFC305ABD0958D55C8AEA308E3285E8224'

                          })

    def parse_pre_fund(self, response):
        yield Request(url='http://www.gfnest.com/index.do')

    def parse_fund(self, response):
        id_list = response.css('div.left li::attr(id)').extract()
        name_list = response.css('div.left li a::text').extract()
        for i, name in zip(id_list, name_list):
            self.ips.append({
                'url': 'http://www.gfnest.com/pm/productinformation_doQueryProByPk.do?pid=%s' % i,
                'ref': response.url,
                'ext': name.replace('【已结束】', '').replace('【到期结束】', '')
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        rows = response.css('table#table1 tr')[1:]
        for r in rows:
            td = r.css('::text').extract()
            row = [_.strip() for _ in td if _.strip()]
            date = row[0]
            nav = row[1]
            add_nav = row[2]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(add_nav) if add_nav else None

            yield item
