# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import FormRequest


class RuiYiInvestSpider(GGFundNavSpider):
    name = 'FundNav_RuiYiInvest'
    sitename = '睿亿投资'
    channel = '投资顾问'

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.ruiyiinvestment.com/product'

    }]

    def start_requests(self):
        yield FormRequest(url='http://www.ruiyiinvestment.com/user/login',
                          formdata={
                              'username': self.username,
                              'password': self.password
                          })

    def parse_fund(self, response):
        href_list = response.css('div.left a::attr(href)').extract()
        for href in href_list:
            self.ips.append({
                'url': 'http://www.ruiyiinvestment.com%s' % href,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.css('div.right tr')[1:]
        for r in rows:
            row = r.css('td::text').extract()
            fund_name = row[0]
            nav = row[1]
            added_nav = row[2]
            date = row[3]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
            yield item
