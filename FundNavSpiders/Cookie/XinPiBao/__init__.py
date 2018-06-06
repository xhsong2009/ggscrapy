import json
from urllib.parse import quote
from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class XinPiBaoSpider(GGFundNavSpider):
    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = r'JSESSIONID=93BB77B439A84E8AA74C39D1BDAD4040; xpbtoken=3agb9spi1tvmfdsq24kuj1j1hqi7l; td_cookie=11049077; Hm_lvt_bd5f74e276d37b338277623405760296=1520998130,1521081411,1521453205,1521604197; Hm_lpvt_bd5f74e276d37b338277623405760296=1521604236'
    org_id = None

    # yield Request(url='http://www.xinpibao.com/sso/api/users/random', callback=self.parse_pre_login)
    # def parse_pre_login(self, response):
    #     yield Request(url='http://www.xinpibao.com/sso/api/users/login',
    #                   method='POST',
    #                   headers={'Content-Type': 'application/x-www-form-urlencoded',
    #                            'Referer': 'http://www.xinpibao.com/sso/'},
    #                   body=b'{"mobile":"13916427906","password":"ZYYXSM123"}',
    #                   callback=self.parse_login)
    #
    # def parse_login(self, response):
    #     pass

    def start_requests(self):
        if isinstance(self.org_id, str):
            yield Request(url='http://www.xinpibao.com/web/api/idmapping/?id=' + self.org_id, callback=self.parse_map)

    def parse_map(self, response):
        flt1 = '{"managerCompanyId":"' + eval(response.text)['data'] + '"}'
        flt1 = quote(flt1)
        flt2 = '{"investCounsellorManagerCompanyId":"' + eval(response.text)['data'] + '"}'
        flt2 = quote(flt2)
        self.fps = [
            {
                'url': 'http://www.xinpibao.com/web/api/funds/computeInfos/?filter=' + flt1 + '&from=0',
                'ref': 'http://www.xinpibao.com/company/' + self.org_id + '.html',
            },
            {
                'url': 'http://www.xinpibao.com/web/api/funds/computeInfos/?filter=' + flt2 + '&from=0',
                'ref': 'http://www.xinpibao.com/company/' + self.org_id + '.html',
            },
        ]

    def parse_fund(self, response):
        funds = json.loads(response.text)['dataList']
        for fund in funds:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']
            item['fund_name'] = fund['fund']['name']

            statistic_date = fund['compute']['lastNetValue']['evaluateDate'][0:8]
            statistic_date = statistic_date[0:4] + '-' + statistic_date[4:6] + '-' + statistic_date[6:8]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = fund['compute']['lastNetValue']['shareUnitValue'] / 10000
            item['nav'] = float(nav) if nav is not None else None

            added_nav = fund['compute']['lastNetValue']['shareUnitAccumulateValue'] / 10000
            item['added_nav'] = float() if added_nav is not None else None
            yield item
            fund_name = fund['fund']['name']
            url_id = fund['fund']['urlId']
            fund_id = fund['id']
            self.ips.append({
                'pg': {'page': 0, 'fund_id': fund_id},
                'url': lambda pg: 'http://www.xinpibao.com/web/api/funds/' + str(
                    pg['fund_id']) + '/netValues?from=' + str(
                    6 * pg['page']),
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                },
                'ref': 'http://www.xinpibao.com/fund/' + url_id + '.html',
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        url = response.meta['url']
        ext = response.meta['ext']
        fund_name = ext['fund_name']

        rows = json.loads(response.text)['dataList']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.request.headers['Referer']
            item['fund_name'] = fund_name

            statistic_date = row['evaluateDate'][0:8]
            statistic_date = statistic_date[0:4] + '-' + statistic_date[4:6] + '-' + statistic_date[6:8]
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            item['nav'] = float(row['shareUnitValue']) / 10000 if row['shareUnitValue'] is not None else None
            item['added_nav'] = float(row['shareUnitAccumulateValue']) / 10000 if row['shareUnitAccumulateValue'] is not None else None
            yield item

        total = json.loads(response.text)['total']
        pg = response.meta['pg']
        if 6 * pg['page'] < total:
            pg['page'] += 1
            self.ips.append({
                'pg': pg,
                'url': url,
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Pragma': 'no-cache'
                },
                'ref': response.request.headers['Referer'],
                'ext': {'fund_name': fund_name},
            })
