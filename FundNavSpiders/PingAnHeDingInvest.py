
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class PingAnHeDingInvestSpider(GGFundNavSpider):
    name = 'FundNav_PingAnHeDingInvest'
    sitename = '平安阖鼎投资'
    channel = '投顾净值'

    fps = [
        {
            'url': 'http://trust.pingan.com/hedingchanpinjingzhi/index.shtml',
            'form': {'currentPageNo': '1'},
            'pg': 1
        }
    ]

    def parse_fund(self, response):
        funds = response.xpath('//table[@id="hdTable"]/tr')[1:]
        for fund in funds:
            fund_code = fund.xpath('./td[last()]/a/@href').re_first('index_(\S+)_1\.shtml')
            fund_name = fund.xpath('./td[2]/text()').extract_first()
            self.ips.append({
                'url': 'http://trust.pingan.com/hedingchanpinjingzhi/index_' + fund_code + '_2.shtml',
                'form': {'trustNo': fund_code, 'pageNo': '1', 'allPage': '2'},

                'ref': response.url,
                'ext': {'fund_name': fund_name},
            })
        pg = response.meta['pg']
        if len(funds) > 1:
            pg += 1
            self.fps.append({
                'url': 'http://trust.pingan.com/hedingchanpinjingzhi/index.shtml',
                'form': {'currentPageNo': str(pg)},
                'ref': response.url,
                'pg': pg
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table[@class="hwp_table m_a"]/tbody/tr')[2:]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            fund_date = row.xpath('./td[2]/text()').extract_first()
            if fund_date is None:
                continue
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')

            nav = row.xpath('./td[4]/text()').re_first('[0-9.]+')
            item['nav'] = float(nav) if nav is not None and nav != '' else None
            added_nav = row.xpath('./td[5]/text()').re_first('[0-9.]+')
            item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
            yield item


