import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class XiangCaiZhengQuanSpider(GGFundNavSpider):
    name = 'FundNav_XiangCaiZhengQuan'
    sitename = '湘财证券'
    channel = '券商资管净值'

    fps = [{
        'url': 'https://ziguan.xcsc.com/main/zcgl/qxcp/DA0001/cpgk.shtml'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//ul[@id="qxcpul"]/li/a')
        for fund in funds:
            fund_name = fund.xpath('./text()').extract_first()
            code = fund.xpath('./@href').re_first('[A-Z]+\d+')

            self.ips.append({
                'url': 'https://ziguan.xcsc.com/servlet/asset/AssetManage',
                'ref': response.url,
                'form': {
                    'function': 'loadFundJz',
                    'fundcode': code,
                    'curPage': '1',
                    'numPerPage': '10',
                    'reqUrl': '/servlet/asset/AssetManage?function=loadFundJz&fundcode=' + code,
                    '_': '1526452208722'
                },
                'ext': {'fund_name': fund_name, 'fund_code': code}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table/tr')
        type = response.xpath('//table/tr[1]/th[2]/text()').extract()
        for row in rows[1:]:
            statistic_date = row.xpath('./td[1]/text()').extract_first()
            if statistic_date is None or statistic_date == '':
                continue
            nav = row.xpath('./td[2]/text()').extract_first()
            added_nav = row.xpath('./td[3]/text()').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
            if '份额净值' in type:
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
            elif '万份收益' in type:
                item['income_value_per_ten_thousand'] = float(nav) if nav is not None and nav != '--' else None
                item['annualized_return'] = float(added_nav.strip('%'))/100.0 if added_nav is not None and added_nav != '--' else None
            yield item

        if len(rows) > int(response.meta['form']['numPerPage']):
            code = response.meta['ext']['fund_code']
            pg = response.meta['form']['curPage']
            pg = int(pg)+1
            self.ips.append({
                'url': 'https://ziguan.xcsc.com/servlet/asset/AssetManage',
                'ref': response.url,
                'form': {
                    'function': 'loadFundJz',
                    'fundcode': code,
                    'curPage': str(pg),
                    'numPerPage': '10',
                    'reqUrl': '/servlet/asset/AssetManage?function=loadFundJz&fundcode=' + code,
                    '_': '1526452208722'
                },
                'ext': {'fund_name': fund_name, 'fund_code': code}
            })
