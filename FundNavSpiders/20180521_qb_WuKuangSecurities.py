# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WuKuangSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_WuKuangSecurities'
    sitename = '五矿证券'
    channel = '券商资管净值'

    trs_keycode = ['233b3c5a-7ebb-4352-9180-7517f1cb641f', '2655a63b-f8ba-4d92-b2c7-4b9e832996b2',
                   '725ec1ba-d48e-4c64-bc12-01a9b9a456cb', '8051637b-a70f-414c-aa6a-99ae103f5b35',
                   '9443378e-c0a2-4b10-bc76-d150fac6a514', 'a15c45e6-059e-4cbd-a664-bb3e8320a5a6',
                   'a4a2a8a6-8743-4188-9e5b-1599e4c55743', 'a5905a55-18b9-4676-8e47-c399e357ef45',
                   'bff21410-16bc-427e-8594-e9a2a8ade197', 'd3b226bd-2e18-4f55-b20d-0a48dc4a2298']

    ips = []
    main_href = 'http://www.wkzq.com.cn/wkzq/news/NewsDetail.aspx?sysClassID=9ae8360a-2ef7-4d30-9c12-cc5b50b0b8d5&id='
    for k in trs_keycode:
        ips.append({
            'url': main_href + k,
        })

    def parse_item(self, response):
        rows = response.css('div.detail_cn tr')[1:]
        for r in rows:
            row_str = ''.join(r.css('td ::text').re('\S+'))
            if '产品' in row_str or '净值' in row_str:
                continue
            if 'a5905a55-18b9-4676-8e47-c399e357ef45' in response.url:
                fund_name = response.css('span#msgTitle::text').re_first('(.*)产品净值')
                date = ''.join(r.css('td:nth-child(1) ::text').re('\S+'))
                nav_a = ''.join(r.css('td:nth-child(2) ::text').re('\S+'))
                add_nav_a = ''.join(r.css('td:nth-child(4) ::text').re('\S+'))
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav_a.replace('．', '.')) if nav_a else None
                item['added_nav'] = float(add_nav_a.replace(' ', '')) if add_nav_a else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

                nav_b = ''.join(r.css('td:nth-child(3) ::text').re('\S+'))
                add_nav_b = ''.join(r.css('td:nth-child(5) ::text').re('\S+'))
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name + '次级'
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav_b.replace('．', '.')) if nav_b else None
                item['added_nav'] = float(add_nav_b.replace(' ', '')) if add_nav_b else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

            else:
                date = ''.join(r.css('td:nth-child(1) ::text').re('\S+'))
                fund_name = ''.join(r.css('td:nth-child(3) ::text').re('\S+'))
                nav = ''.join(r.css('td:nth-child(4) ::text').re('\S+'))
                add_nav = ''.join(r.css('td:nth-child(5) ::text').re('\S+'))
                if '和而泰员工持股计划' == fund_name:
                    fund_code = ''.join(r.css('td:nth-child(2) ::text').re('\S+'))
                    fund_name = fund_name + fund_code

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav.replace('．', '.')) if nav else None
                item['added_nav'] = float(add_nav.replace(' ', '')) if add_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None

                yield item
