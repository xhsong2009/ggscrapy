from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
import re


class XingYeTrustSpider(GGFundNavSpider):
    name = 'FundNav_XingYeTrust'
    channel = '信托净值'

    fps = [
        {
            'url': 'http://www.ciit.com.cn/xingyetrust-web/netvalues/netvalues!getValue?type=1&currentpage=1',
            'ref': 'http://www.ciit.com.cn/',
            'ext': {'sitename': '兴业信托1'},
            'pg': 1
        },
        {
            'url': 'http://www.ciit.com.cn/xingyetrust-web/netvalues/netvalues!getValue?type=0&currentpage=1',
            'ref': 'http://www.ciit.com.cn/',
            'ext': {'sitename': '兴业信托2'},
            'pg': 1
        }
    ]

    def parse_fund(self, response):
        sitename = response.meta['ext']['sitename']
        funds = response.xpath('//table[@class="pro_table"]/tr/td[2]/a')
        for fund in funds:
            fund_code = fund.xpath('./@href').re_first('fundCode=(\S+)\&')
            fund_name = fund.xpath('./text()').extract_first()
            self.ips.append({
                'url': 'http://www.ciit.com.cn/funds-struts/fund-net-chart-table/{}?page=1-200'.format(fund_code),
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'sitename': sitename}
            })
        pg = response.meta['pg']
        tp = response.xpath('//a[contains(text(), "尾页")]/@href').re_first('\d+')
        if tp is not None:
            if pg < int(tp):
                pg += 1
                url = re.sub('currentpage=\d+', 'currentpage=' + str(pg), response.url)
                self.fps.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'sitename': sitename},
                    'pg': pg
                })

    def parse_item(self, response):
        sitename = response.meta['ext']['sitename']
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table[@class="table2"]/tr')[1:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath('./td[1]').re_first('\d+-\d+-\d+')
            if statistic_date is None:
                continue
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath('./td[2]').re_first('>\s*([0-9.]+)\s*<')
            item['nav'] = float(nav) if nav is not None else None

            yield item
