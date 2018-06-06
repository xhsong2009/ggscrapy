from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class XiZangTrustSpider(GGFundNavSpider):
    name = 'FundNav_XiZangTrust'
    sitename = '西藏信托'
    channel = '信托净值'

    fps = [{
        'url': 'http://www.ttco.cn/ttco/page_networth',
        'ref': None,
        'form': {'st': 'dd', 'netWorthPage.pageSize': '500', 'netWorthPage.pageNum': '1'}
    }]

    def parse_fund(self, response):
        funds = response.xpath('//div[@class="mainDetail"]/table/tr')[1:]
        for fund in funds:
            id = fund.xpath('./td[1]/a/@href').re_first('id=(\S+)')
            fund_name = fund.xpath('./td[1]/a/text()').extract_first()
            self.ips.append({
                'url': 'http://www.ttco.cn/ttco/networthList?netWorthNetPage.start=0&product.id={}'.format(id),
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'pg': 0, 'id': id}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        id = response.meta['ext']['id']
        rows = response.xpath('//table[@class="valueList"]/tr')[1:]
        for row in rows:
            statistic_date = row.xpath('./td[1]/text()').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[2]/text()').re_first('([0-9.]+)')
            added_nav = row.xpath('./td[3]/text()').re_first('([0-9.]+)')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            statistic_date = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date is not None else None
            item['statistic_date'] = statistic_date
            yield item
        ext = response.meta['ext']
        pg = ext['pg']
        tpg = response.xpath('//a[text()= "尾页"]/@href').re_first('start=(\d+)\&')
        if tpg and pg * 10 < int(tpg):
            ext['pg'] += 1
            self.ips.append({
                'url': 'http://www.ttco.cn/ttco/networthList?netWorthNetPage.start={}&product.id={}'.format(
                    ext['pg'] * 10, id),
                'ref': response.url,
                'ext': ext
            })
