from datetime import datetime
from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class BeijingxingshiInvestSpider(GGFundNavSpider):
    name = 'FundNav_BeijingxingshiInvest'
    sitename = '星石投资'
    channel = '投顾净值'

    username = '18625981663'
    password = '123456zyl'
    cookies = 'ASP.NET_SessionId=23esbiiusvgdl055nj3yyjrr; Remember=True; Cookie_U_Account=18625981663; Cookie_U_Name=123456; Cookie_U_Password=29CE6030B1ECE8380076972342D23745; Cookie_U_Group=1; Cookie_U_Level=1; Cookie_U_Phone=18625981663'
    fps = [{
        'url': 'http://www.starrockinvest.com/xs/invest/wproductinfo?id=1'
    }]

    def parse_fund(self, response):
        urls = response.xpath('//li[@id="all"]/ul/li')
        for url in urls:
            code = url.xpath('./a/@name').extract_first()
            fund_name = url.xpath('./a/text()').extract_first()
            self.ips.append({
                'url': 'http://www.starrockinvest.com/xs/invest/wproductinfo?id=' + str(code) + '&page=1',
                'ref': response.url,
                'ext': {'code': code, 'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        code = ext['code']
        fund_names = ext['fund_name']
        rows = response.xpath('//table[@class="pl2"]//tr[position()>1]')

        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_names

            statistic_date = row.xpath("./td[1]/text()").re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

            nav = row.xpath('./td[2]/text()').extract_first()
            item['nav'] = float(nav) if nav else None

            yield item

        next_url = response.xpath('//span[@class="fr"]/a[text()="下一页"]/@href').extract_first()
        if next_url != 'javascript:void(0)':
            url = urljoin('http://www.starrockinvest.com', next_url)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'code': code, 'fund_name': fund_names}
            })
