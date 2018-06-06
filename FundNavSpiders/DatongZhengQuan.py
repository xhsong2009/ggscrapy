from datetime import datetime
import json
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class DatongZhengQuanSpider(GGFundNavSpider):
    name = 'FundNav_DatongZhengQuan'
    sitename = '大同证券'
    channel = '券商资管净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'https://sc.dtsbc.com.cn:8908/servlet/json',
        'form': {'funcNo': '1001997', 'page': '1', 'numPerPage': '10'},
        'headers': {'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
    }]

    def parse_fund(self, response):
        results = json.loads(response.text)['results']
        if results:
            result = results[0]
            totalPages = result['totalPages']
            currentPage = result['currentPage']
            funds = result['data']
            if funds:
                for fund in funds:
                    product_code = fund['product_code']
                    fund_name = fund['product_name']
                    self.ips.append({
                        'url': 'https://sc.dtsbc.com.cn:8908/servlet/json',
                        'ref': response.url,
                        'form': {'funcNo': '1001998', 'product_code': product_code, 'page': '1', 'numPerPage': '20'},
                        'headers': {'X-Requested-With': 'XMLHttpRequest',
                                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                    },
                        'ext': {'fund_name': fund_name, 'product_code': product_code}
                    })

            if int(currentPage) < int(totalPages):
                self.fps.append({
                    'url': 'https://sc.dtsbc.com.cn:8908/servlet/json',
                    'form': {'funcNo': '1001997', 'page': str(int(currentPage) + 1), 'numPerPage': '10'},
                    'headers': {'X-Requested-With': 'XMLHttpRequest',
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                }
                })

    def parse_item(self, response):
        meta = response.meta['ext']
        fund_name = meta['fund_name']
        product_code = meta['product_code']
        results = json.loads(response.text)['results']
        if results:
            result = results[0]
            totalPages = result['totalPages']
            currentPage = result['currentPage']
            rows = result['data']
            if rows:
                for row in rows:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name

                    statistic_date = row['nav_date']
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                    income_value_per_ten_thousand = row['profit_per_million']
                    if income_value_per_ten_thousand:
                        income_value_per_ten_thousand = income_value_per_ten_thousand.replace('-', '')
                    if income_value_per_ten_thousand != ''and ','not in income_value_per_ten_thousand:
                        item['income_value_per_ten_thousand'] = float(
                            income_value_per_ten_thousand) if income_value_per_ten_thousand is not None else None
                    d7_annualized_return = row['seven_days_annual_profit']
                    if d7_annualized_return:
                        d7_annualized_return = d7_annualized_return.replace('-', '')
                    if d7_annualized_return != '':
                        item['d7_annualized_return'] = float(
                            d7_annualized_return) if d7_annualized_return is not None else None
                    nav = row['nav']
                    if nav:
                        nav = nav.replace('-', '')
                    if nav != '':
                        item['nav'] = float(nav) if nav is not None else None
                    added_nav = row['total_nav']
                    if added_nav:
                        added_nav = added_nav.replace('-', '')
                    if added_nav != '':
                        item['added_nav'] = float(added_nav) if added_nav is not None else None
                    yield item

            if int(currentPage) < int(totalPages):
                self.ips.append({
                    'url': 'https://sc.dtsbc.com.cn:8908/servlet/json',
                    'ref': response.url,
                    'form': {'funcNo': '1001998', 'product_code': product_code, 'page': str(int(currentPage) + 1),
                             'numPerPage': '20'},
                    'headers': {'X-Requested-With': 'XMLHttpRequest',
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                },
                    'ext': {'fund_name': fund_name, 'product_code': product_code}
                })
