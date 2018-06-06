from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class ZhongYinGuoJiStockSpider(GGFundNavSpider):
    name = 'FundNav_ZhongYinGuoJiStock'
    sitename = '中银国际'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.bocichina.com/boci/asset/mfinancing/productIntro.jsp?productCode=A80001&forthMenu=qtcd_asset_jhlc_one_cpjj&secondMenu=qtcd_asset_jhlc'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//td[@background="/boci/pic/gk_10.jpg"]/a')
        for fund in funds[0:1]:
            code = fund.xpath('./@onclick').re_first(r'productCode=(\S+)\'')
            if code is None:
                code = 'A80001'
            fund_name = fund.xpath('./text()').re_first(r'·(\S+)')
            url = 'http://www.bocichina.com/boci/colNetValueAction.do?method=list&productCode=' + code
            url = url + '&forthMenu=qtcd_asset_jhlc_' + code
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'page': '1', 'url': url, 'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        page = int(ext['page'])
        base_url = ext['url']
        rows = response.xpath('//td[@bgcolor="#ffffff"]')
        if rows and len(rows) > 1:
            rows = rows[1]
            rows = rows.xpath('.//tr')
            head_row = rows[0].xpath('./td/text()').re('\S+')
            if rows and len(rows) > 1:
                for row in rows[1:]:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url

                    statistic_date = row.xpath('./td[1]/text()').extract_first()
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

                    if head_row.count('单位净值') > 0:
                        nav = row.xpath('./td[2]/text()').extract_first()
                        item['nav'] = float(nav) if nav else None
                    if head_row.count('累计净值') > 0:
                        added_nav = row.xpath('./td[3]/text()').extract_first()
                        item['added_nav'] = float(added_nav) if added_nav else None
                    if head_row.count('每万份收益') > 0:
                        income_value_per_ten_thousand = row.xpath('./td[2]/text()').extract_first()
                        item['income_value_per_ten_thousand'] = float(
                            income_value_per_ten_thousand) if income_value_per_ten_thousand else None
                    if head_row.count('七日年化收益率') > 0:
                        d7_annualized_return = row.xpath('./td[3]/text()').re_first('(\d+\.?\d*)')
                        item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return else None
                    yield item
                url = base_url + '&pagesize=10&currentPage=' + str(page + 1)
                self.ips.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'page': str(page + 1), 'url': base_url, 'fund_name': fund_name}
                })
