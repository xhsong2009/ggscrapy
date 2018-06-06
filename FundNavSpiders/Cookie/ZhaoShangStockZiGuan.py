import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhaoShangStockZiGuanSpider(GGFundNavSpider):
    name = 'FundNav_ZhaoShangStockZiGuan'
    sitename = '招商证券资管'
    channel = '券商资管净值'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'PLAY_SESSION=f308296c260bd1aa0ccbd588f56c76ff5a6dde96-%00___ID%3Aa11e7ff9-716f-4d05-a58d-c723db286382%00; cms_yht="VzDPKfPg4frpftbZoX/06Be9wTToSt5i1R3WGKF32d3FCchL22vYoDj6LaXu7njImZoLpkvzDeM+@doeFsGvgORFP/iiTGwo5ZpGXMhRDdgXplX8gSAqaXiUYanFSvr3QkLhluQMzpyP6fwy7PqfbUWYX@oi7ewNHwRELDj2B9bxw="'

    fps = [{
        'url': 'https://amc.cmschina.com/p/productlist',
        'form': {'limit': '2000'},
        'ref': 'https://amc.cmschina.com/',
    }]

    def parse_fund(self, response):
        funds = json.loads(response.text)['data']['rows']
        for fund in funds:
            fund_name = fund['name_abbrev']
            type_code = fund['type_code']
            fund_id = fund['fund_id']
            url = 'https://amc.cmschina.com/licai/jz'
            self.ips.append({
                'url': url,
                'ref': response.url,
                'form': {'fund_id': fund_id,
                         'page': '1',
                         'startdate': '',
                         'enddate': ''},
                'ext': {'fund_name': fund_name, 'page': '1', 'fund_id': str(fund_id), 'type_code': type_code}
            })

    def parse_item(self, response):
        datas = json.loads(response.text)
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        type_code = ext['type_code']
        page = int(ext['page'])
        fund_id = ext['fund_id']
        if datas is not None and datas['data']['rows'] is not None:
            datas = datas['data']['rows']
            if len(datas) > 0:
                url = 'https://amc.cmschina.com/licai/jz'
                self.ips.append({
                    'url': url,
                    'ref': response.url,
                    'form': {'fund_id': fund_id,
                             'page': str(page + 1),
                             'startdate': '',
                             'enddate': ''},
                    'ext': {'fund_name': fund_name, 'page': str(page + 1), 'fund_id': str(fund_id),
                            'type_code': type_code}
                })
            for data in datas:
                statistic_date = data[2]
                nav = data[3]
                added_nav = data[4]
                annualized_return = data[14]
                d7_annualized_return = data[7]
                income_value_per_ten_thousand = data[5]
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = 'https://amc.cmschina.com/licai/detail?fund_id={}'.format(fund_id)
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
                if type_code == '1':
                    item['annualized_return'] = float(
                        annualized_return) if annualized_return is not None and annualized_return != '' else None
                elif type_code == '2':
                    item['d7_annualized_return'] = float(
                        d7_annualized_return) if d7_annualized_return is not None and d7_annualized_return != '' else None
                    item['income_value_per_ten_thousand'] = float(
                        income_value_per_ten_thousand) if income_value_per_ten_thousand is not None and income_value_per_ten_thousand != '' else None
                else:
                    item['nav'] = float(nav) if nav is not None and nav != '' else None
                    item['added_nav'] = float(added_nav) if added_nav is not None and nav != '' else None
                yield item
