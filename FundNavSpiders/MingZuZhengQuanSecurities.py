# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class MingZuZhengQuanSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_MingZuZhengQuanSecurities'
    sitename = '民族证券'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.e5618.com/mzzq/zcgl/public/left.jsp',
        'form': {'classid': '0001000100010008000400020001'}
    }]

    def parse_fund(self, response):
        class_id = response.css('div.zcgl_menu02 a::attr(href)').re('classid=(.*)')
        fund_name = response.css('div.zcgl_menu02 a::text').extract()
        for f_name, c_id in zip(fund_name, class_id):
            self.ips.append({
                'url': 'http://www.e5618.com/mzzq/zcgl/public/cpNavContent.jsp',
                'form': {
                    'classid': c_id + '0003',
                    'type': '2',
                    'pageIndex': '1'
                },
                'pg': 1,
                'ext': f_name
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        rows = response.css('tr')[2:]
        col_type = response.css('tr th::text').extract()
        if rows:
            for r in rows:
                row = r.css('td::text').extract()
                date = row[0]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None

                if '单位净值' in col_type:
                    item['nav'] = float(row[1]) if row[1] else None
                    item['added_nav'] = float(row[2]) if row[2] else None
                elif '7日年化' in col_type:
                    item['d7_annualized_return'] = float(row[1]) if row[1] else None
                    item['income_value_per_ten_thousand'] = float(row[2]) if row[2] else None

                yield item

            next_pg = response.meta['pg'] + 1
            meta = response.meta
            meta['pg'] = next_pg
            meta['form']['pageIndex'] = str(next_pg)
            self.ips.append(meta)
