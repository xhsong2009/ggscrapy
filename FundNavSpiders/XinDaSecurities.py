from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class XinDaSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_XinDaSecurities'
    sitename = '信达证券'
    channel = '券商资管净值'

    fps = [
        {
            'url': 'http://www.cindasc.com/servlet/json?funcNo=2000025&currentPage=1&numPerPage=500',
        }
    ]

    def parse_fund(self, response):
        funds = json.loads(response.text)['DataSet0']
        for fund in funds:
            fund_code = fund['productcode']
            fund_name = fund['productname']
            self.ips.append({
                'url': 'http://www.cindasc.com/servlet/json?funcNo=2000023&ispage=y&numPerPage=500&productcode={}&currentPage=1'.format(fund_code),
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'fund_code': fund_code},
                'pg': 1
            })

    def parse_item(self, response):
        fund_code = response.meta['ext']['fund_code']
        fund_name = response.meta['ext']['fund_name']
        rows = json.loads(response.text)['DataSet0']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = row['networth_date']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            if fund_name == '信达现金宝集合资产管理计划':
                d7_annualized_return = row['newnav']
                item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return is not None else None
            else:
                nav = row['newnav']
                item['nav'] = float(nav) if nav is not None else None

                added_nav = row['totalnav']
                item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item
        tp = json.loads(response.text)['DataSet1'][0]['total_pages']
        pg = response.meta['pg']
        if pg < int(tp):
            pg += 1
            self.ips.append({
                'url': 'http://www.cindasc.com/servlet/json?funcNo=2000023&ispage=y&numPerPage=500&productcode={0}&currentPage={1}'.format(fund_code, pg),
                'ext': response.meta['ext']
            })

