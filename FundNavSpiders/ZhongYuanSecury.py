# -*- coding: utf-8 -*-

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ZhongYuanSecurySpider(GGFundNavSpider):
    name = 'FundNav_ZhongYuanSecury'
    sitename = '中原证券'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.ccnew.com/main/assetMng/xetdcp/xhyh/index.shtml',
        'ref': 'http://www.ccnew.com/',
        'ext': {'type': 0}
    }]

    def parse_fund(self, response):

        type = response.meta['ext']['type']
        if type == 0:
            funds = response.xpath('//div[@class="spmain"]//ul/li//a')
            for fund in funds:
                url = fund.xpath("./@href").extract_first()
                fund_name = fund.xpath("./text()").extract_first()
                if 'javascript' not in url:
                    self.fps.append({
                        'url': urljoin(get_base_url(response), url),
                        'ref': response.url,
                        'ext': {'fund_name': fund_name, 'type': 1}
                    })
        else:
            id = response.xpath('//a[contains(.//text(), "产品净值查询")]/@onclick').re_first('ajaxLoadArticle\((\d+)\)')
            fund_name = response.meta['ext']['fund_name']
            if id:
                self.ips.append({
                    'url': 'http://www.ccnew.com/cgi-bin/article/Article?function=ajaxArticlePage&product=product&ispage=yes&catalogId='+ id,
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table/tr')[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = row.xpath('./td[3]//text()').re_first('\d+-\d+-\d+')
            if statistic_date is None:
                continue
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            if '七日年化收益率' in response.text:
                income_value_per_ten_thousand = row.xpath('./td[1]').re_first('>\s*([0-9.]+)\s*<')
                item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand)if income_value_per_ten_thousand else None

                d7_annualized_return = row.xpath('./td[2]').re_first('>\s*([0-9.]+)\s*<')
                item['d7_annualized_return'] = float(d7_annualized_return)if d7_annualized_return else None

            else:
                nav = row.xpath('./td[1]').re_first('>\s*([0-9.]+)\s*<')
                item['nav'] = float(nav) if nav is not None else None
                added_nav = row.xpath('./td[2]').re_first('>\s*([0-9.]+)\s*<')
                item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item




